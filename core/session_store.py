"""
session_store.py — Riwayat percakapan persisten (untuk --continue / --resume).

Sesi disimpan sebagai JSON di <data>/sessions/<id>.json (sadar-profil via paths.py):
  { "id": "...", "title": "...", "created_at": int, "updated_at": int,
    "messages": [ {"role": "user|assistant", "content": "...", "t": int}, ... ] }
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import paths


def _dir() -> Path:
    return paths.sessions_dir()


def new_id() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def path_of(sid: str) -> Path:
    return _dir() / f"{sid}.json"


def create(title: str = "") -> dict:
    sid = new_id()
    s = {"id": sid, "title": title or sid, "created_at": int(time.time()),
         "updated_at": int(time.time()), "messages": []}
    save(s)
    return s


def save(s: dict) -> None:
    s["updated_at"] = int(time.time())
    path_of(s["id"]).write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")


def load(sid: str) -> dict | None:
    p = path_of(sid)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def append(s: dict, role: str, content: str) -> None:
    s.setdefault("messages", []).append({"role": role, "content": content, "t": int(time.time())})
    if role == "user" and (not s.get("title") or s["title"] == s["id"]):
        s["title"] = content[:48]
    save(s)


def latest() -> dict | None:
    files = sorted(_dir().glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    return load(files[0].stem) if files else None


def list_sessions(limit: int = 20) -> list[dict]:
    files = sorted(_dir().glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)[:limit]
    out = []
    for f in files:
        s = load(f.stem)
        if s:
            out.append({"id": s["id"], "title": s.get("title", s["id"]),
                        "turns": len(s.get("messages", [])), "updated_at": s.get("updated_at", 0)})
    return out


def history_text(s: dict, max_turns: int = 8, max_chars: int = 2000) -> str:
    msgs = s.get("messages", [])[-max_turns:]
    txt = "\n".join(f"{m['role']}: {m['content']}" for m in msgs)
    return txt[-max_chars:]
