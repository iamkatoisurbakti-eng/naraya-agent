from pathlib import Path
import shutil
import hashlib
import json
import time
import subprocess

ROOT = Path("/root/naraya-agent")
HERMES = Path("/root/.hermes")
IMPORT_DIR = ROOT / "data/hermes-import"
STATE_FILE = ROOT / "data/hermes_sync_state.json"
CHANGED_LIST = ROOT / "data/hermes_changed_files.json"
LOG = ROOT / "logs/hermes_incremental_sync.log"

INCLUDE = [
    "SOUL.md",
    ".hermes_history",
    "berita-daily.txt",
    "memories",
    "sessions",
    "skills",
]

BLOCKED_PARTS = [
    ".env",
    "auth.json",
    "secret",
    "token",
    "credential",
    "whatsapp",
    "cache",
    ".lock",
    ".pid",
    ".tmp",
    "state.db",
]

def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{int(time.time())}] {msg}"
    print(line)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def is_safe(path: Path):
    raw = str(path).lower()
    return not any(x in raw for x in BLOCKED_PARTS)

def file_hash(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

def iter_files():
    for item in INCLUDE:
        base = HERMES / item
        if not base.exists():
            continue

        if base.is_file():
            if is_safe(base):
                yield base
        else:
            for f in base.rglob("*"):
                if f.is_file() and is_safe(f):
                    yield f

def copy_changed():
    old_state = load_state()
    new_state = {}
    changed = []

    IMPORT_DIR.mkdir(parents=True, exist_ok=True)

    for src in iter_files():
        rel = src.relative_to(HERMES).as_posix()
        dst = IMPORT_DIR / rel

        try:
            h = file_hash(src)
        except Exception as e:
            log(f"skip hash error {rel}: {e}")
            continue

        new_state[rel] = h

        if old_state.get(rel) == h and dst.exists():
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        changed.append(rel)
        log(f"changed/copied: {rel}")

    save_state(new_state)

    CHANGED_LIST.write_text(
        json.dumps(changed, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    log(f"changed files: {len(changed)}")
    return changed

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
        log(result.stdout[-3000:])

    if result.stderr:
        log("STDERR: " + result.stderr[-3000:])

    if result.returncode != 0:
        raise RuntimeError(cmd)

def main():
    log("=== HERMES INCREMENTAL SYNC START ===")

    changed = copy_changed()

    if not changed:
        log("no changes, skip import/rag")
        log("=== HERMES INCREMENTAL SYNC DONE ===")
        return

    run("/root/naraya-agent/.venv/bin/python build_skill_registry.py")

    run("/root/naraya-agent/.venv/bin/python import_hermes_safe.py")
    run("/root/naraya-agent/.venv/bin/python build_rag_incremental.py")

    log("=== HERMES INCREMENTAL SYNC DONE ===")

if __name__ == "__main__":
    main()
