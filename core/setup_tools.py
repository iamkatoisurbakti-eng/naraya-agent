"""
setup_tools.py — Pasang semua dependensi tool Naraya-Agent sekali jalan.

Jalankan:  python core/setup_tools.py
Opsi   :  python core/setup_tools.py --no-browser   (lewati unduh Chromium)

Memasang: httpx, mcp, openai, pyautogui, pillow, playwright, python-dotenv,
apscheduler, chromadb, openai-agents (untuk runtime agen), lalu Chromium Playwright.
Aman diulang (idempinten).
"""

from __future__ import annotations

import subprocess
import sys

PACKAGES = [
    "httpx",
    "mcp",
    "openai",
    "openai-agents",
    "anthropic",
    "pyautogui",
    "pillow",
    "playwright",
    "python-dotenv",
    "apscheduler",
    "chromadb",
    # paket pendukung tambahan
    "aiohttp",
    "certifi",
    "markdown",
    "pathspec",
    "pydantic-core",
    "pyjwt",
    "starlette",
    "urllib3",
]


def run(cmd: list[str]) -> int:
    print(">", " ".join(cmd))
    return subprocess.call(cmd)


def main() -> None:
    no_browser = "--no-browser" in sys.argv

    print("=== Pasang paket Python ===")
    rc = run([sys.executable, "-m", "pip", "install", "--upgrade", *PACKAGES])
    if rc != 0:
        print("Sebagian paket gagal dipasang. Coba ulang atau pasang manual.")

    if not no_browser:
        print("\n=== Unduh browser Chromium untuk Playwright (sekali saja) ===")
        run([sys.executable, "-m", "playwright", "install", "chromium"])
    else:
        print("\n(lewati unduh Chromium)")

    print("\nSelesai. Verifikasi status tiap tool dengan:")
    print("   python core/selftest_tools.py")


if __name__ == "__main__":
    main()
