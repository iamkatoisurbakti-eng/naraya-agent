"""
skills_index.py — Indeks & pencocokan SKILLS yang dimiliki Naraya-Agent.

Sumber (dicoba berurutan, tahan-banting):
  1. data/hermes_skill_registry.json  (list-of-dict ATAU dict-berisi-list)
  2. scan skills/**/SKILL.md           (ambil frontmatter name/description/category)

Fungsi utama:
  load_skills()          -> list[{name, description, category}]
  relevant(goal, k=6)    -> list skill paling relevan (skor overlap kata)
  relevant_text(goal, k) -> teks ringkas untuk disuntik ke konteks agen

Dipakai orkestrasi agar agen "selalu memakai skills yang ada" bila relevan.
"""

from __future__ import annotations

import re
import json
from pathlib import Path

_CACHE: list[dict] | None = None

_REG = Path("data/hermes_skill_registry.json")
_SKILLS_DIRS = [Path("skills"), Path("../skills")]

_STOP = set("the a an dan di ke yang untuk dengan dari pada atau buat bikin agar bisa "
            "saya kamu ini itu and or to for of in on with create make build".split())


def _norm(d: dict) -> dict:
    """Seragamkan satu entri skill ke {name, description, category} apa pun bentuk aslinya."""
    name = d.get("name") or d.get("skill") or d.get("title") or d.get("id") or ""
    desc = d.get("description") or d.get("desc") or d.get("summary") or ""
    cat = d.get("category") or d.get("group") or d.get("kategori") or ""
    return {"name": str(name), "description": str(desc)[:300], "category": str(cat)}


def _from_registry() -> list[dict]:
    if not _REG.exists():
        return []
    try:
        data = json.loads(_REG.read_text(encoding="utf-8"))
    except Exception:
        return []
    items: list = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        # cari list pertama di dalam dict, atau perlakukan dict-of-dict
        for v in data.values():
            if isinstance(v, list):
                items = v
                break
        else:
            items = [dict(v, name=k) if isinstance(v, dict) else {"name": k} for k, v in data.items()]
    out = []
    for it in items:
        if isinstance(it, dict):
            out.append(_norm(it))
        elif isinstance(it, str):
            out.append({"name": it, "description": "", "category": ""})
    return [s for s in out if s["name"]]


def _parse_frontmatter(text: str) -> dict:
    d = {}
    m = re.search(r"^---\s*(.*?)\s*---", text, re.DOTALL)
    block = m.group(1) if m else text[:600]
    for key in ("name", "description", "category"):
        mm = re.search(rf"^{key}\s*:\s*(.+)$", block, re.MULTILINE | re.IGNORECASE)
        if mm:
            d[key] = mm.group(1).strip().strip('"').strip("'")
    return d


def _from_files() -> list[dict]:
    out = []
    for base in _SKILLS_DIRS:
        if not base.exists():
            continue
        for f in base.rglob("SKILL.md"):
            try:
                fm = _parse_frontmatter(f.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                fm = {}
            name = fm.get("name") or f.parent.name
            out.append({"name": name, "description": fm.get("description", "")[:300],
                        "category": fm.get("category", f.parent.parent.name if f.parent.parent else "")})
        if out:
            break
    return out


def load_skills(force: bool = False) -> list[dict]:
    global _CACHE
    if _CACHE is not None and not force:
        return _CACHE
    skills = _from_registry()
    if not skills:
        skills = _from_files()
    _CACHE = skills
    return skills


def _tokens(s: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if len(w) > 2 and w not in _STOP}


def relevant(goal: str, k: int = 6) -> list[dict]:
    """Skill paling relevan dengan goal (skor overlap kata pada name+description+category)."""
    skills = load_skills()
    if not skills:
        return []
    gt = _tokens(goal)
    if not gt:
        return skills[:k]
    scored = []
    for s in skills:
        st = _tokens(s["name"] + " " + s["description"] + " " + s["category"])
        score = len(gt & st)
        # bonus bila kata goal muncul di nama skill
        score += sum(2 for w in gt if w in s["name"].lower())
        if score:
            scored.append((score, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [s for _, s in scored[:k]]


def relevant_text(goal: str, k: int = 6) -> str:
    rs = relevant(goal, k)
    if not rs:
        return "(tidak ada skill terindeks)"
    return "\n".join(f"- {s['name']}" + (f": {s['description']}" if s['description'] else "") for s in rs)


if __name__ == "__main__":
    import sys
    g = " ".join(sys.argv[1:]) or "buat aplikasi web dengan deployment dan testing"
    print("total skill terindeks:", len(load_skills()))
    print("relevan untuk:", g)
    print(relevant_text(g))
