"""
benchmark_engine.py — Harness evaluasi NYATA untuk Naraya-Agent.

Pengganti versi lama yang hanya mencocokkan string ("VALIDATION" in result -> +20).
Sekarang setiap task dinilai dua lapis:

  1. Deterministik (0-50): berapa banyak `checks` (regex) yang terpenuhi pada
     jawaban agent. Objektif, tidak bisa "dicurangi" prompt.
  2. LLM-judge (0-50): model menilai kualitas jawaban terhadap `rubric`.

Total per task 0-100; skor benchmark = rata-rata seluruh task.
Setiap run disimpan ke tabel `benchmark_runs` di data/evolution.db.

Cara kerja: sebuah *system prompt* kandidat diuji dengan menjalankannya pada
seluruh task (agent menjawab pakai prompt itu), lalu dinilai. Inilah yang
membuat evolusi prompt bisa diukur secara nyata.

Backward-compatible: fungsi `benchmark()` tetap ada dan mengembalikan float.
"""

from __future__ import annotations

import re
import json
import time
import sqlite3
from pathlib import Path

import llm
import prompt_store

TASKS_FILE = Path("core/eval/tasks.json")
TASKS_FILE_ALT = Path("eval/tasks.json")
DB_PATH = Path("data/evolution.db")


def _load_tasks() -> list[dict]:
    path = TASKS_FILE if TASKS_FILE.exists() else TASKS_FILE_ALT
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["tasks"]


def _ensure_db() -> None:
    Path("data").mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS benchmark_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score REAL,
            num_tasks INTEGER,
            detail TEXT,
            prompt_hash TEXT,
            created_at INTEGER
        )
        """
    )
    conn.commit()
    conn.close()


def _deterministic_score(answer: str, task: dict) -> tuple[float, int, int]:
    checks = task.get("checks", [])
    if not checks:
        return 50.0, 0, 0
    matched = 0
    for pattern in checks:
        try:
            if re.search(pattern, answer, re.IGNORECASE):
                matched += 1
        except re.error:
            if pattern.lower() in answer.lower():
                matched += 1
    score = (matched / len(checks)) * 50.0
    return round(score, 2), matched, len(checks)


_JUDGE_SYSTEM = (
    "Kamu adalah evaluator ketat dan adil. Nilai jawaban kandidat terhadap rubric. "
    "Keluarkan JSON: {\"score\": <0-50 integer>, \"reason\": \"<alasan singkat>\"}. "
    "Skor 50 = sempurna sesuai rubric; 0 = gagal total."
)


def _judge_score(answer: str, task: dict) -> tuple[float, str]:
    user = (
        f"PERTANYAAN:\n{task['prompt']}\n\n"
        f"RUBRIC:\n{task.get('rubric', 'Nilai kualitas, akurasi, dan relevansi.')}\n\n"
        f"JAWABAN KANDIDAT:\n{answer}\n\n"
        "Beri skor 0-50."
    )
    result = llm.chat_json(
        user,
        system=_JUDGE_SYSTEM,
        model=llm.JUDGE_MODEL,
        default={"score": 0, "reason": "judge gagal parse"},
    )
    try:
        score = float(result.get("score", 0))
    except (TypeError, ValueError):
        score = 0.0
    score = max(0.0, min(50.0, score))
    return round(score, 2), str(result.get("reason", ""))[:300]


def evaluate_prompt(system_prompt: str, use_judge: bool = True) -> dict:
    tasks = _load_tasks()
    details = []
    total = 0.0

    for task in tasks:
        answer = llm.chat(task["prompt"], system=system_prompt, temperature=0.2)

        det_score, matched, n_checks = _deterministic_score(answer, task)

        if use_judge:
            judge, reason = _judge_score(answer, task)
        else:
            judge, reason = 0.0, "judge dimatikan"

        task_total = round(det_score + judge, 2)
        total += task_total

        details.append(
            {
                "id": task["id"],
                "category": task.get("category"),
                "deterministic": det_score,
                "checks": f"{matched}/{n_checks}",
                "judge": judge,
                "judge_reason": reason,
                "total": task_total,
                "answer_preview": answer[:200],
            }
        )

    avg = round(total / len(tasks), 2) if tasks else 0.0
    return {"score": avg, "num_tasks": len(tasks), "details": details}


def _save_run(result: dict, system_prompt: str) -> None:
    _ensure_db()
    import hashlib

    phash = hashlib.sha256(system_prompt.encode()).hexdigest()[:12]
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        INSERT INTO benchmark_runs (score, num_tasks, detail, prompt_hash, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            result["score"],
            result["num_tasks"],
            json.dumps(result["details"], ensure_ascii=False),
            phash,
            int(time.time()),
        ),
    )
    conn.commit()
    conn.close()


def run_benchmark(system_prompt: str | None = None, use_judge: bool = True, save: bool = True) -> dict:
    if system_prompt is None:
        system_prompt = prompt_store.get_active_prompt()
    result = evaluate_prompt(system_prompt, use_judge=use_judge)
    if save:
        _save_run(result, system_prompt)
    return result


def benchmark() -> float:
    return run_benchmark()["score"]


if __name__ == "__main__":
    if not llm.is_available():
        print("[offline] Tidak ada API key — set OPENAI_API_KEY untuk menjalankan benchmark nyata.")
    else:
        res = run_benchmark()
        print(f"SKOR BENCHMARK: {res['score']}/100 ({res['num_tasks']} task)\n")
        for d in res["details"]:
            print(f"  {d['id']:<20} total={d['total']:<6} det={d['deterministic']} judge={d['judge']} ({d['checks']})")
