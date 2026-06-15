from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path("/root/naraya-agent")
HERMES = Path("/root/.hermes")
IMPORT_DIR = ROOT / "data/hermes-import"
LOG = ROOT / "logs/hermes_daily_sync.log"

INCLUDE_PATHS = [
    "SOUL.md",
    ".hermes_history",
    "berita-daily.txt",
    "memories",
    "sessions",
    "skills",
]

def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{int(time.time())}] {msg}"
    print(line)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def safe_copy():
    IMPORT_DIR.mkdir(parents=True, exist_ok=True)

    for name in INCLUDE_PATHS:
        src = HERMES / name
        dst = IMPORT_DIR / name

        if not src.exists():
            log(f"skip missing: {name}")
            continue

        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()

        if src.is_dir():
            shutil.copytree(
                src,
                dst,
                ignore=shutil.ignore_patterns(
                    ".env",
                    "auth.json",
                    "*secret*",
                    "*token*",
                    "*credential*",
                    "whatsapp",
                    "cache",
                    "*.lock",
                    "*.pid",
                    "*.tmp",
                    "state.db*",
                )
            )
        else:
            shutil.copy2(src, dst)

        log(f"copied: {name}")

def run(cmd):
    log("run: " + cmd)

    result = subprocess.run(
        cmd,
        shell=True,
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        timeout=1800,
    )

    if result.stdout:
        log(result.stdout[-2000:])

    if result.stderr:
        log("STDERR: " + result.stderr[-2000:])

    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def main():
    log("=== HERMES DAILY SYNC START ===")

    safe_copy()

    run("/root/naraya-agent/.venv/bin/python import_hermes_safe.py")
    run("/root/naraya-agent/.venv/bin/python build_rag.py")

    log("=== HERMES DAILY SYNC DONE ===")

if __name__ == "__main__":
    main()
