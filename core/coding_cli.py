"""
coding_cli.py — Integrasi agen coding eksternal: Claude Code & OpenAI Codex.

Naraya bisa mendelegasikan tugas coding ke CLI ini (headless / non-interaktif):
  • Claude Code : `claude -p "<prompt>"`   (paket npm: @anthropic-ai/claude-code, butuh ANTHROPIC_API_KEY/login)
  • Codex       : `codex exec "<prompt>"`  (paket npm: @openai/codex, butuh OPENAI_API_KEY/login)

Semua aman: bila CLI/Node belum terpasang atau kunci tak ada, fungsi mengembalikan
pesan + cara setup, bukan crash.
"""

from __future__ import annotations

import os
import shutil
import subprocess

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def _cwd() -> str:
    return os.getenv("NARAYA_HOME") or os.getcwd()


def _which(name: str) -> str | None:
    return shutil.which(name)


def _run(args: list[str], timeout: int) -> str:
    try:
        p = subprocess.run(args, cwd=_cwd(), capture_output=True, text=True, timeout=timeout)
        out = (p.stdout or "") + (("\nSTDERR:\n" + p.stderr) if p.stderr else "")
        return out.strip() or f"(selesai, rc {p.returncode})"
    except subprocess.TimeoutExpired:
        return f"TIMEOUT: melebihi {timeout} detik."
    except Exception as exc:
        return f"ERROR menjalankan {args[0]}: {exc}"


def claude_code(prompt: str, timeout: int = 600) -> str:
    """Delegasikan tugas coding ke Claude Code (headless). Mengembalikan output teks."""
    exe = _which("claude")
    if not exe:
        return ("Claude Code belum terpasang. Install: `npm install -g @anthropic-ai/claude-code` "
                "lalu set ANTHROPIC_API_KEY (atau `claude` untuk login). "
                "Atau jalankan: naraya install-coders")
    if not (os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_CODE_OAUTH_TOKEN")):
        # tetap dicoba (mungkin sudah login lokal), tapi beri petunjuk bila gagal
        pass
    return _run([exe, "-p", prompt], timeout)


def codex(prompt: str, timeout: int = 600) -> str:
    """Delegasikan tugas coding ke OpenAI Codex (non-interaktif `codex exec`)."""
    exe = _which("codex")
    if not exe:
        return ("Codex belum terpasang. Install: `npm install -g @openai/codex` "
                "lalu set OPENAI_API_KEY (atau `codex` untuk login). "
                "Atau jalankan: naraya install-coders")
    return _run([exe, "exec", prompt], timeout)


def status() -> str:
    """Status terpasang/tidaknya agen coding eksternal."""
    node = _which("node") or _which("nodejs")
    lines = [
        f"node    : {'ada (' + node + ')' if node else 'TIDAK ADA — pasang Node.js dulu'}",
        f"claude  : {'ada' if _which('claude') else 'belum (npm i -g @anthropic-ai/claude-code)'}",
        f"codex   : {'ada' if _which('codex') else 'belum (npm i -g @openai/codex)'}",
        f"ANTHROPIC_API_KEY: {'ada' if os.getenv('ANTHROPIC_API_KEY') else 'belum'}",
        f"OPENAI_API_KEY   : {'ada' if os.getenv('OPENAI_API_KEY') else 'belum'}",
    ]
    return "\n".join(lines)


def install_coding_clis() -> str:
    """Pasang Claude Code & Codex via npm (global). Butuh Node.js/npm."""
    npm = _which("npm")
    if not npm:
        return ("npm/Node.js belum terpasang.\n"
                "Ubuntu/Debian: sudo apt install -y nodejs npm\n"
                "Windows/macOS: pasang dari https://nodejs.org , lalu ulangi.")
    results = []
    for pkg in ("@anthropic-ai/claude-code", "@openai/codex"):
        try:
            rc = subprocess.call([npm, "install", "-g", pkg])
            results.append(f"{pkg}: {'OK' if rc == 0 else 'gagal (rc ' + str(rc) + ')'}")
        except Exception as exc:
            results.append(f"{pkg}: error {exc}")
    return "Hasil pemasangan:\n  " + "\n  ".join(results) + "\n\n" + status()


if __name__ == "__main__":
    print(status())
