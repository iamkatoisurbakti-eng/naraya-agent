"""
prompt_store.py — Penyimpanan persisten untuk "system prompt terbaik" Naraya-Agent.

Kenapa ada:
- Evolusi prompt jadi tidak berguna kalau hasilnya tidak disimpan & dipakai.
- File ini menyimpan prompt aktif di `data/prompts/system_prompt.txt`
  dan mencatat seluruh riwayat versi (beserta skornya) di tabel SQLite.

Dipakai oleh:
- benchmark_engine.py  -> mengevaluasi prompt aktif
- evolution_engine.py  -> menyimpan prompt kandidat yang terbukti lebih baik
- agen runtime         -> bisa memuat prompt aktif via get_active_prompt()
"""

from __future__ import annotations

import time
import sqlite3
from pathlib import Path

DATA_DIR = Path("data")
PROMPT_DIR = DATA_DIR / "prompts"
ACTIVE_FILE = PROMPT_DIR / "system_prompt.txt"
DB_PATH = DATA_DIR / "evolution.db"

# Prompt awal (baseline) — sengaja sederhana supaya evolusi punya ruang naik.
DEFAULT_PROMPT = (
    "Kamu adalah Naraya-Agent, asisten AI berbahasa Indonesia yang fokus pada "
    "pekerjaan nyata dan otomasi.\n"
    "- Klarifikasi dulu: bila permintaan belum lengkap detailnya (mis. 'buatkan landing page' "
    "tanpa tema, judul, gaya, target, atau konten), JANGAN langsung kerjakan — ajukan 2-4 "
    "pertanyaan singkat dan tunggu jawaban; kecuali user bilang 'langsung saja'.\n"
    "- Jawab ringkas, jelas, dan akurat.\n"
    "- Gunakan Bahasa Indonesia yang natural.\n"
    "- Ikuti instruksi format dengan tepat.\n"
    "- Tolak permintaan yang ilegal atau berbahaya secara sopan."
)


def _ensure() -> None:
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS prompt_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            score REAL,
            source TEXT,
            active INTEGER,
            created_at INTEGER
        )
        """
    )
    conn.commit()
    conn.close()


def get_active_prompt() -> str:
    """Ambil prompt aktif; inisialisasi dengan DEFAULT_PROMPT bila belum ada."""
    _ensure()
    if ACTIVE_FILE.exists():
        text = ACTIVE_FILE.read_text(encoding="utf-8", errors="ignore").strip()
        if text:
            return text
    set_active_prompt(DEFAULT_PROMPT, score=None, source="default")
    return DEFAULT_PROMPT


def set_active_prompt(prompt: str, score: float | None = None, source: str = "evolution") -> None:
    """Tetapkan prompt aktif baru dan catat ke riwayat."""
    _ensure()
    prompt = prompt.strip()
    ACTIVE_FILE.write_text(prompt, encoding="utf-8")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE prompt_versions SET active = 0")
    conn.execute(
        """
        INSERT INTO prompt_versions (prompt, score, source, active, created_at)
        VALUES (?, ?, ?, 1, ?)
        """,
        (prompt, score, source, int(time.time())),
    )
    conn.commit()
    conn.close()


def history(limit: int = 20) -> list[dict]:
    """Riwayat versi prompt terbaru lebih dulu."""
    _ensure()
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        """
        SELECT id, score, source, active, created_at
        FROM prompt_versions
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "score": r[1],
            "source": r[2],
            "active": bool(r[3]),
            "created_at": r[4],
        }
        for r in rows
    ]


if __name__ == "__main__":
    print("=== ACTIVE PROMPT ===")
    print(get_active_prompt())
    print("\n=== HISTORY ===")
    for h in history():
        print(h)
