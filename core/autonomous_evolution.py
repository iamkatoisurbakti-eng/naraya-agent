"""
autonomous_evolution.py — Siklus belajar otonom Naraya-Agent (versi nyata).

Perbaikan dari versi lama:
  - Tidak lagi memanggil `sched.start()` saat MODULE DI-IMPORT.
  - Satu siklus = benchmark -> refine memory -> evolve prompt -> self-play.
  - Guardrail: berhenti aman bila offline; catat tiap siklus ke log file.
  - `run_cycle()` bisa dipanggil manual (sekali jalan).

Loop terjadwal : python core/autonomous_evolution.py
Sekali jalan   : python core/autonomous_evolution.py --once
Interval       : NARAYA_EVO_INTERVAL_MIN=30 python core/autonomous_evolution.py
"""

from __future__ import annotations

import os
import sys
import json
import time
from pathlib import Path

import llm
from benchmark_engine import run_benchmark
from evolution_engine import evolve
from refine_memory import refine
from self_play import run_self_play

LOG_FILE = Path("logs/evolution_cycles.log")

_no_improvement_streak = 0


def _log(record: dict) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    record["time"] = int(time.time())
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_cycle() -> dict:
    global _no_improvement_streak

    if not llm.is_available():
        rec = {"status": "offline", "message": "Tidak ada API key; siklus dilewati."}
        _log(rec)
        return rec

    bench = run_benchmark()

    try:
        refine()
        refine_ok = True
    except Exception as exc:
        refine_ok = f"skip: {exc}"

    evo = evolve()
    sp = run_self_play()

    if evo.get("applied"):
        _no_improvement_streak = 0
    else:
        _no_improvement_streak += 1

    rec = {
        "status": "ok",
        "benchmark_score": bench["score"],
        "evolution": evo,
        "refine": refine_ok,
        "self_play_saved": sum(1 for r in sp if isinstance(r, dict) and r.get("saved")),
        "no_improvement_streak": _no_improvement_streak,
    }
    _log(rec)
    return rec


def _run_scheduler() -> None:
    from apscheduler.schedulers.blocking import BlockingScheduler

    interval_min = int(os.getenv("NARAYA_EVO_INTERVAL_MIN") or os.getenv("NUSANTARA_EVO_INTERVAL_MIN") or "60")
    sched = BlockingScheduler()

    @sched.scheduled_job("interval", minutes=interval_min)
    def _job():
        print("\n=== AUTONOMOUS CYCLE ===")
        print(json.dumps(run_cycle(), ensure_ascii=False, indent=2))

    print(f"NARAYA EVOLUTION ACTIVE (tiap {interval_min} menit). Ctrl+C untuk berhenti.")
    print(json.dumps(run_cycle(), ensure_ascii=False, indent=2))
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nEvolution dihentikan.")


if __name__ == "__main__":
    if "--once" in sys.argv:
        print(json.dumps(run_cycle(), ensure_ascii=False, indent=2))
    else:
        _run_scheduler()
