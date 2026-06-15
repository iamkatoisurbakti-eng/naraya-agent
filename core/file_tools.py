"""
file_tools.py — Operasi berkas untuk Naraya-Agent: baca, tulis, tambah, edit, hapus, jelajah.

Pengaman: operasi dibatasi pada FOLDER KERJA (env NARAYA_FILE_ROOT, default cwd).
Path di luar folder ditolak kecuali NARAYA_FILE_ALLOW_OUTSIDE=1. Menghapus root dilarang.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path


def _root() -> Path:
    return Path(os.getenv("NARAYA_FILE_ROOT") or os.getcwd()).resolve()


def _allow_outside() -> bool:
    return os.getenv("NARAYA_FILE_ALLOW_OUTSIDE", "").lower() in ("1", "true", "yes")


def _resolve(path: str) -> Path:
    p = Path(path)
    return (p if p.is_absolute() else _root() / p).resolve()


def _guard(p: Path) -> str | None:
    if _allow_outside():
        return None
    try:
        p.relative_to(_root())
        return None
    except ValueError:
        return f"DITOLAK: '{p}' di luar folder kerja ({_root()}). Set NARAYA_FILE_ALLOW_OUTSIDE=1 untuk mengizinkan."


def read_file(path: str, max_bytes: int = 100_000) -> str:
    """Baca isi berkas teks."""
    p = _resolve(path)
    if (e := _guard(p)):
        return e
    if not p.exists():
        return f"Tidak ada: {p}"
    if p.is_dir():
        return f"'{p}' adalah folder — pakai daftar_file."
    try:
        data = p.read_text(encoding="utf-8", errors="replace")
        return data[:max_bytes] + ("\n…(dipotong)" if len(data) > max_bytes else "")
    except Exception as exc:
        return f"ERROR baca: {exc}"


def write_file(path: str, content: str) -> str:
    """Buat/timpa berkas dengan isi tertentu (folder dibuat otomatis)."""
    p = _resolve(path)
    if (e := _guard(p)):
        return e
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Ditulis: {p} ({len(content.encode('utf-8'))} B)"
    except Exception as exc:
        return f"ERROR tulis: {exc}"


def append_file(path: str, content: str) -> str:
    """Tambahkan teks ke akhir berkas (buat bila belum ada)."""
    p = _resolve(path)
    if (e := _guard(p)):
        return e
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as f:
            f.write(content)
        return f"Ditambah ke: {p}"
    except Exception as exc:
        return f"ERROR tambah: {exc}"


def edit_file(path: str, find: str, replace: str, count: int = 0) -> str:
    """Edit berkas: ganti teks `find` menjadi `replace` (count=0 = semua kemunculan)."""
    p = _resolve(path)
    if (e := _guard(p)):
        return e
    if not p.exists():
        return f"Tidak ada: {p}"
    try:
        s = p.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return f"ERROR baca: {exc}"
    if find not in s:
        return f"Teks tidak ditemukan di {p.name}; tidak ada perubahan."
    n = s.count(find) if count == 0 else min(count, s.count(find))
    s2 = s.replace(find, replace) if count == 0 else s.replace(find, replace, count)
    try:
        p.write_text(s2, encoding="utf-8")
        return f"Diedit: {p} ({n} penggantian)"
    except Exception as exc:
        return f"ERROR tulis: {exc}"


def delete_file(path: str) -> str:
    """Hapus berkas atau folder (rekursif). Tidak bisa menghapus folder root."""
    p = _resolve(path)
    if (e := _guard(p)):
        return e
    if p == _root() or p == Path(p.anchor):
        return "DITOLAK: tidak boleh menghapus folder root/kerja."
    if not p.exists():
        return f"Tidak ada: {p}"
    try:
        if p.is_dir():
            shutil.rmtree(p)
            return f"Folder dihapus: {p}"
        p.unlink()
        return f"Dihapus: {p}"
    except Exception as exc:
        return f"ERROR hapus: {exc}"


def make_dir(path: str) -> str:
    """Buat folder (beserta induknya)."""
    p = _resolve(path)
    if (e := _guard(p)):
        return e
    try:
        p.mkdir(parents=True, exist_ok=True)
        return f"Folder dibuat: {p}"
    except Exception as exc:
        return f"ERROR buat folder: {exc}"


def move_file(src: str, dst: str) -> str:
    """Pindah/ganti nama berkas atau folder."""
    s, d = _resolve(src), _resolve(dst)
    if (e := _guard(s)) or (e := _guard(d)):
        return e
    if not s.exists():
        return f"Tidak ada: {s}"
    try:
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(s), str(d))
        return f"Dipindah: {s} -> {d}"
    except Exception as exc:
        return f"ERROR pindah: {exc}"


def list_dir(path: str = ".") -> str:
    """Daftar isi folder."""
    p = _resolve(path)
    if (e := _guard(p)):
        return e
    if not p.exists():
        return f"Tidak ada: {p}"
    if p.is_file():
        return f"{p.name} (file, {p.stat().st_size} B)"
    items = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
    if not items:
        return f"{p}: (kosong)"
    lines = []
    for x in items:
        if x.is_dir():
            lines.append(f"  [DIR] {x.name}/")
        else:
            try:
                lines.append(f"        {x.name}  ({x.stat().st_size} B)")
            except Exception:
                lines.append(f"        {x.name}")
    return f"{p}:\n" + "\n".join(lines)


if __name__ == "__main__":
    print(list_dir("."))
