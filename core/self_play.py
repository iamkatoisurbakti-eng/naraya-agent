"""
self_play.py — Self-play berbasis debat yang DINILAI dan DISIMPAN terukur.

Versi lama hanya men-`print()` hasil debat. Sekarang:
  - Setiap topik didebatkan (politik vs ekonomi vs validator) lalu disintesis.
  - Hasil sintesis DINILAI oleh LLM-judge (0-100).
  - Hanya insight dengan skor >= QUALITY_THRESHOLD yang disimpan ke knowledge base.
  - Semua run dicatat ke tabel `self_play_runs` (skor + apakah disimpan).

Catatan: modul legacy (debate_engine/synthesis_engine) yang meng-import `openai`
di-level atas baru diimpor di dalam fungsi, agar jalur OFFLINE tetap aman.
"""

from __future__ import annotations

import time
import json
import sqlite3
from pathlib import Path

import llm

DB_PATH = Path("data/naraya_memory.db")
QUALITY_THRESHOLD = 70.0

TOPICS = [
    "Strategi otomasi AI yang realistis untuk bisnis kecil",
    "Peluang dan risiko AI dalam ekonomi digital Asia Tenggara",
    "Bagaimana agen AI lokal menjaga keamanan data pengguna",
]

_JUDGE_SYSTEM = (
    "Kamu evaluator strategi. Nilai hasil sintesis debat ini. "
    "Keluarkan JSON: {\"score\": <0-100 integer>, \"reason\": \"<alasan singkat>\"}. "
    "Skor tinggi bila insight akurat, seimbang, dan actionable; rendah bila dangkal "
    "atau mengandung klaim yang meragukan."
)


def _ensure_db() -> None:
    Path("data").mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS self_play_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            score REAL,
            saved INTEGER,
            reason TEXT,
            created_at INTEGER
        )
        """
    )
    conn.commit()
    conn.close()


def _judge(topic: str, synthesis: str) -> tuple[float, str]:
    user = f"TOPIK:\n{topic}\n\nHASIL SINTESIS:\n{synthesis}\n\nBeri skor 0-100."
    result = llm.chat_json(
        user, system=_JUDGE_SYSTEM, model=llm.JUDGE_MODEL,
        default={"score": 0, "reason": "judge gagal"},
    )
    try:
        score = float(result.get("score", 0))
    except (TypeError, ValueError):
        score = 0.0
    return max(0.0, min(100.0, score)), str(result.get("reason", ""))[:300]


def _run_one(topic: str) -> dict:
    # import legacy ditunda ke sini supaya import modul ini aman saat offline
    from debate_engine import ask_agent
    from synthesis_engine import synthesize
    from debate_memory import save_debate_knowledge

    politik = ask_agent("Agent Politik", topic)
    ekonomi = ask_agent("Agent Ekonomi", topic)
    validator = ask_agent(
        "Agent Validator",
        f"POLITIK:\n{politik}\n\nEKONOMI:\n{ekonomi}\n\nApa yang paling kuat dan apa kelemahannya?",
    )
    debate_text = f"=== POLITIK ===\n{politik}\n\n=== EKONOMI ===\n{ekonomi}\n\n=== VALIDATOR ===\n{validator}"
    synthesis = synthesize(topic, debate_text)

    score, reason = _judge(topic, synthesis)
    saved = 0
    if score >= QUALITY_THRESHOLD:
        save_debate_knowledge(topic, synthesis)
        saved = 1

    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO self_play_runs (topic, score, saved, reason, created_at) VALUES (?, ?, ?, ?, ?)",
        (topic, score, saved, reason, int(time.time())),
    )
    conn.commit()
    conn.close()

    return {"topic": topic, "score": score, "saved": bool(saved), "reason": reason}


def run_self_play(topics: list[str] | None = None) -> list[dict]:
    if not llm.is_available():
        return [{"status": "offline", "message": "Tidak ada API key; self-play dilewati."}]

    results = []
    for topic in (topics or TOPICS):
        results.append(_run_one(topic))
    return results


if __name__ == "__main__":
    print(json.dumps(run_self_play(), ensure_ascii=False, indent=2))
