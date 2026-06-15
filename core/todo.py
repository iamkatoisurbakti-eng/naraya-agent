"""
todo.py — Daftar tugas (to-do) untuk Naraya-Agent.

Persisten & sadar-profil (disimpan di <data>/todos.json). Bisa dikelola:
  - oleh agen lewat tool (tugas_tetapkan / tugas_selesai / tugas_lihat),
  - oleh pengguna lewat CLI `naraya todo ...` atau slash `/todo` di REPL.

Status item: pending [ ] · doing [~] · done [x].
"""

from __future__ import annotations

import json
from pathlib import Path

import paths

_SYM = {"pending": "[ ]", "doing": "[~]", "done": "[x]"}


def _file() -> Path:
    return paths.data_dir() / "todos.json"


def load() -> list[dict]:
    f = _file()
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save(items: list[dict]) -> None:
    _file().write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def set_items(tasks: list) -> list[dict]:
    items = [{"task": str(t).strip(), "status": "pending"} for t in (tasks or []) if str(t).strip()]
    save(items)
    return items


def add(task: str) -> list[dict]:
    items = load()
    items.append({"task": str(task).strip(), "status": "pending"})
    save(items)
    return items


def mark(idx: int, status: str = "done") -> list[dict]:
    items = load()
    if 1 <= idx <= len(items):
        items[idx - 1]["status"] = status
        save(items)
    return items


def done(idx: int) -> list[dict]:
    return mark(idx, "done")


def doing(idx: int) -> list[dict]:
    return mark(idx, "doing")


def clear() -> list[dict]:
    save([])
    return []


def stats(items: list[dict] | None = None) -> tuple[int, int]:
    items = load() if items is None else items
    return sum(1 for it in items if it.get("status") == "done"), len(items)


def render(items: list[dict] | None = None) -> str:
    items = load() if items is None else items
    if not items:
        return "(tidak ada tugas)"
    d, n = stats(items)
    head = f"To-do ({d}/{n} selesai):"
    body = "\n".join(f"  {_SYM.get(it.get('status'), '[ ]')} {i}. {it.get('task','')}"
                     for i, it in enumerate(items, 1))
    return head + "\n" + body


if __name__ == "__main__":
    print(render())
