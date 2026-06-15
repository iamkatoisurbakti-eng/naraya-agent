from pathlib import Path
import json

SOURCE_DIR = Path("data/hermes-import")
OUTPUT_FILE = Path("data/hermes_knowledge.md")

ALLOWED_EXT = {
    ".txt", ".md", ".json", ".yaml", ".yml",
    ".html", ".log"
}

SKIP_NAMES = {
    ".env", "auth.json", "gateway.lock", "gateway.pid"
}

MAX_FILE_CHARS = 15000

def read_file(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if path.suffix.lower() == ".json":
            try:
                data = json.loads(text)
                text = json.dumps(data, ensure_ascii=False, indent=2)
            except Exception:
                pass
        return text[:MAX_FILE_CHARS]
    except Exception as e:
        return f"[GAGAL BACA: {path} | {e}]"

def is_allowed(path: Path) -> bool:
    if path.name in SKIP_NAMES:
        return False
    if path.suffix.lower() not in ALLOWED_EXT and not path.name.startswith("Byte"):
        return False

    raw = str(path).lower()
    blocked = [
        "whatsapp/session",
        "auth",
        "secret",
        "token",
        "credential",
        ".env",
        "state.db",
        "cache",
    ]

    return not any(x in raw for x in blocked)

def main():
    chunks = []

    for file in SOURCE_DIR.rglob("*"):
        if not file.is_file():
            continue
        if not is_allowed(file):
            continue

        content = read_file(file).strip()
        if not content:
            continue

        chunks.append(
            f"\n\n# FILE: {file}\n\n"
            f"```text\n{content}\n```"
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(chunks), encoding="utf-8")

    print(f"OK: {OUTPUT_FILE}")
    print(f"Total file masuk: {len(chunks)}")

if __name__ == "__main__":
    main()
