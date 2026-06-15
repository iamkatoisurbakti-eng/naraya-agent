"""
evolution_engine.py — Optimasi prompt NYATA (pengganti versi `score + 5` palsu).

Alur sesungguhnya:
  1. Ambil prompt aktif (baseline) dan ukur skornya pada benchmark.
  2. Identifikasi task yang lemah dari hasil baseline.
  3. Minta LLM mengusulkan N kandidat system-prompt yang memperbaiki kelemahan itu.
  4. Ukur tiap kandidat pada benchmark yang sama.
  5. Terapkan kandidat HANYA jika skornya benar-benar > baseline + MIN_DELTA.
  6. Catat angka before/after yang sebenarnya ke evolution.db.
"""

from __future__ import annotations

import llm
import prompt_store
from benchmark_engine import run_benchmark
from evolution_db import save_evolution

MIN_DELTA = 1.0
WEAK_THRESHOLD = 70.0
DEFAULT_CANDIDATES = 2


_PROPOSE_SYSTEM = (
    "Kamu adalah perekayasa prompt (prompt engineer) ahli. Tugasmu memperbaiki "
    "system prompt sebuah agen AI berbahasa Indonesia agar skornya naik pada "
    "evaluasi otomatis. Pertahankan yang sudah baik, perbaiki yang lemah. "
    "Keluarkan JSON: {\"prompt\": \"<system prompt baru lengkap>\"}."
)


def _weak_summary(details: list[dict]) -> str:
    weak = [d for d in details if d.get("total", 0) < WEAK_THRESHOLD]
    if not weak:
        return "Tidak ada kelemahan menonjol; cari perbaikan marginal yang aman."
    lines = []
    for d in weak:
        lines.append(
            f"- Task '{d['id']}' (kategori {d.get('category')}): total {d['total']}/100 "
            f"[checks {d.get('checks')}, judge {d.get('judge')}] — alasan judge: {d.get('judge_reason','')}"
        )
    return "Task yang masih lemah:\n" + "\n".join(lines)


def _propose_candidate(baseline_prompt: str, weak_summary: str, variant: int) -> str | None:
    user = (
        f"SYSTEM PROMPT SAAT INI:\n\"\"\"\n{baseline_prompt}\n\"\"\"\n\n"
        f"HASIL EVALUASI:\n{weak_summary}\n\n"
        f"Buat versi ke-{variant} dari system prompt yang lebih baik. Fokus menutup "
        "kelemahan di atas tanpa merusak kemampuan lain. Jaga tetap ringkas dan jelas."
    )
    result = llm.chat_json(user, system=_PROPOSE_SYSTEM, temperature=0.6, default={})
    prompt = (result or {}).get("prompt", "").strip()
    return prompt or None


def evolve(num_candidates: int = DEFAULT_CANDIDATES) -> dict:
    if not llm.is_available():
        return {"status": "offline", "message": "Tidak ada API key; evolusi dilewati."}

    baseline_prompt = prompt_store.get_active_prompt()
    baseline = run_benchmark(baseline_prompt)
    score_before = baseline["score"]
    weak = _weak_summary(baseline["details"])

    best_prompt = None
    best_score = score_before
    attempts = []

    for i in range(1, num_candidates + 1):
        candidate = _propose_candidate(baseline_prompt, weak, i)
        if not candidate:
            attempts.append({"variant": i, "status": "no_prompt"})
            continue

        cand_result = run_benchmark(candidate)
        cand_score = cand_result["score"]
        attempts.append({"variant": i, "score": cand_score})

        if cand_score > best_score:
            best_score = cand_score
            best_prompt = candidate

    applied = 0
    if best_prompt is not None and best_score > score_before + MIN_DELTA:
        prompt_store.set_active_prompt(best_prompt, score=best_score, source="evolution")
        applied = 1

    save_evolution(
        component="system_prompt",
        old_version=baseline_prompt,
        new_version=best_prompt if best_prompt else baseline_prompt,
        score_before=score_before,
        score_after=best_score,
        applied=applied,
    )

    return {
        "status": "ok",
        "score_before": score_before,
        "score_after": best_score,
        "improvement": round(best_score - score_before, 2),
        "applied": bool(applied),
        "attempts": attempts,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(evolve(), ensure_ascii=False, indent=2))
