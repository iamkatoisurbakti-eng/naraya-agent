"""
naraya_daemon.py — Daemon 24/7: self-evaluation + self-learning untuk Naraya-Agent.

Dua loop terjadwal terpisah:
  • SELF-EVALUATION (tiap NARAYA_EVAL_INTERVAL_MIN, default 60 mnt):
        jalankan benchmark nyata -> catat skor & detail ke log + DB.
  • SELF-LEARNING   (tiap NARAYA_LEARN_INTERVAL_MIN, default 180 mnt):
        refine memori -> evolusi prompt (terukur) -> self-play (insight tersaring)
        -> reindex skills. Hanya menerapkan perubahan bila skor benar-benar naik.

Sifat: offline-safe (tanpa API key, loop mencatat status 'offline' dan menunggu),
tidak ada efek samping saat di-import (scheduler hanya jalan via __main__).

Jalankan 24 jam:
    python core/naraya_daemon.py
    NARAYA_EVAL_INTERVAL_MIN=30 NARAYA_LEARN_INTERVAL_MIN=120 python core/naraya_daemon.py
Sekali jalan (uji):
    python core/naraya_daemon.py --once
"""

from __future__ import annotations

import os
import sys
import json
import time
from pathlib import Path

LOG_FILE = Path("logs/daemon.log")


def _log(rec: dict) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    rec["time"] = int(time.time())
    rec["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps(rec, ensure_ascii=False))


def _online() -> bool:
    try:
        import llm
        return llm.is_available()
    except Exception:
        return False


def eval_cycle() -> dict:
    """SELF-EVALUATION: ukur kualitas agen sekarang via benchmark."""
    if not _online():
        rec = {"cycle": "eval", "status": "offline"}
        _log(rec)
        return rec
    try:
        from benchmark_engine import run_benchmark
        res = run_benchmark()
        rec = {"cycle": "eval", "status": "ok", "score": res["score"], "num_tasks": res["num_tasks"]}
    except Exception as exc:
        rec = {"cycle": "eval", "status": "error", "error": str(exc)[:160]}
    _log(rec)
    return rec


def learn_cycle() -> dict:
    """SELF-LEARNING: refine memori, evolusi prompt terukur, self-play, reindex skills."""
    if not _online():
        rec = {"cycle": "learn", "status": "offline"}
        _log(rec)
        return rec
    out: dict = {"cycle": "learn", "status": "ok"}
    # 1) refine memori jangka panjang
    try:
        from refine_memory import refine
        refine()
        out["refine"] = "ok"
    except Exception as exc:
        out["refine"] = f"skip: {str(exc)[:80]}"
    # 2) evolusi prompt (hanya diterapkan bila skor naik)
    try:
        from evolution_engine import evolve
        out["evolution"] = evolve()
    except Exception as exc:
        out["evolution"] = f"skip: {str(exc)[:80]}"
    # 3) self-play -> insight tersaring
    try:
        from self_play import run_self_play
        sp = run_self_play()
        out["self_play_saved"] = sum(1 for r in sp if isinstance(r, dict) and r.get("saved"))
    except Exception as exc:
        out["self_play"] = f"skip: {str(exc)[:80]}"
    # 4) reindex skills (agar pencocokan skill selalu terbaru)
    try:
        import skills_index
        out["skills_indexed"] = len(skills_index.load_skills(force=True))
    except Exception as exc:
        out["skills"] = f"skip: {str(exc)[:80]}"
    _log(out)
    return out


def run_once() -> dict:
    return {"eval": eval_cycle(), "learn": learn_cycle()}


def main() -> None:
    if "--once" in sys.argv:
        print(json.dumps(run_once(), ensure_ascii=False, indent=2))
        return

    eval_min = int(os.getenv("NARAYA_EVAL_INTERVAL_MIN", "60"))
    learn_min = int(os.getenv("NARAYA_LEARN_INTERVAL_MIN", "180"))

    try:
        from apscheduler.schedulers.blocking import BlockingScheduler
    except Exception:
        print("apscheduler belum terpasang: pip install apscheduler")
        print("Fallback: loop manual sederhana.")
        _manual_loop(eval_min, learn_min)
        return

    sched = BlockingScheduler()
    sched.add_job(eval_cycle, "interval", minutes=eval_min, id="eval")
    sched.add_job(learn_cycle, "interval", minutes=learn_min, id="learn")
    _log({"cycle": "daemon", "status": "start", "eval_min": eval_min, "learn_min": learn_min,
          "online": _online()})
    # jalankan sekali di awal
    eval_cycle()
    learn_cycle()
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        _log({"cycle": "daemon", "status": "stop"})


def _manual_loop(eval_min: int, learn_min: int) -> None:
    last_learn = 0.0
    while True:
        eval_cycle()
        if time.time() - last_learn >= learn_min * 60:
            learn_cycle()
            last_learn = time.time()
        time.sleep(eval_min * 60)


if __name__ == "__main__":
    main()
