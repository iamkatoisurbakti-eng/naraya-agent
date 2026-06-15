"""
workspace_writer.py — Tulis hasil project ke folder workspace, bukan ke terminal.

Agen coding/backend/frontend diinstruksikan mengeluarkan berkas dalam format:
    === FILE: path/relatif/nama.ext ===
    ```bahasa
    <isi kode>
    ```

Modul ini mengekstrak blok itu, menulisnya ke workspace/<timestamp>-<slug>/,
dan menyimpan laporan lengkap ke REPORT.md. Terminal cukup menampilkan ringkasan.
"""

from __future__ import annotations

import re
import time
from pathlib import Path

_FILE_RE = re.compile(r"===\s*FILE:\s*(.+?)\s*===\s*\n```[^\n]*\n(.*?)```", re.DOTALL)


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return (s[:40] or "project")


def _safe_rel(path: str) -> str:
    """Cegah path traversal; kembalikan path relatif aman."""
    p = (path or "").strip().replace("\\", "/").lstrip("/")
    parts = [x for x in p.split("/") if x not in ("..", "", ".")]
    return "/".join(parts) or "file.txt"


def extract_files(text: str) -> list[tuple[str, str]]:
    out = []
    for m in _FILE_RE.finditer(text or ""):
        out.append((_safe_rel(m.group(1)), m.group(2)))
    return out


def has_files(result: dict) -> bool:
    return any(extract_files(v) for v in (result.get("report") or {}).values())


def write_project(result: dict, base: str = "workspace") -> dict:
    """Tulis semua berkas dari hasil orkestrasi ke folder project. Kembalikan ringkasan."""
    goal = result.get("goal", "project")
    proj = Path(base) / f"{time.strftime('%Y%m%d-%H%M%S')}-{slug(goal)}"
    proj.mkdir(parents=True, exist_ok=True)

    written: dict[str, int] = {}
    # urutan dict = urutan agen; revisi (coding#rev1) otomatis menimpa versi awal
    for _key, out in (result.get("report") or {}).items():
        for rel, content in extract_files(out):
            f = proj / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(content, encoding="utf-8")
            written[rel] = len(content.encode("utf-8"))

    # simpan laporan lengkap (termasuk kode) ke file, bukan ke terminal
    try:
        import multi_agent
        (proj / "REPORT.md").write_text(multi_agent.format_report(result), encoding="utf-8")
    except Exception:
        pass

    return {"dir": str(proj), "files": [{"path": p, "bytes": b} for p, b in written.items()]}
