"""
paths.py — Lokasi data yang sadar-profil (untuk fitur Hermes-like).

Profil dipilih lewat env NARAYA_PROFILE (default: "default").
Tiap profil punya data dir terpisah → sesi & pilihan provider/model terisolasi.
  default              -> data/
  profil "kerja"       -> data/profiles/kerja/
"""

from __future__ import annotations

import os
from pathlib import Path


def profile() -> str:
    return os.getenv("NARAYA_PROFILE", "default") or "default"


def data_dir() -> Path:
    p = Path("data") if profile() == "default" else Path("data") / "profiles" / profile()
    p.mkdir(parents=True, exist_ok=True)
    return p


def sessions_dir() -> Path:
    d = data_dir() / "sessions"
    d.mkdir(parents=True, exist_ok=True)
    return d
