from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
import hashlib
import json

load_dotenv()

client = OpenAI()

ROOT = Path("/root/naraya-agent")
IMPORT_DIR = ROOT / "data/hermes-import"
CHANGED_LIST = ROOT / "data/hermes_changed_files.json"

DB_DIR = str(ROOT / "data/chroma_db")
COLLECTION = "hermes_knowledge"

ALLOWED_EXT = {
    ".txt", ".md", ".json", ".yaml", ".yml",
    ".html", ".log"
}

def chunk_text(text, max_chars=3000, overlap=300):
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start = end - overlap

    return chunks

def embed(text):
    result = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return result.data[0].embedding

def read_file(path: Path):
    return path.read_text(encoding="utf-8", errors="ignore")

def allowed(path: Path):
    if path.name.startswith("Byte"):
        return True
    return path.suffix.lower() in ALLOWED_EXT

def main():
    if not CHANGED_LIST.exists():
        print("No changed list.")
        return

    changed = json.loads(CHANGED_LIST.read_text(encoding="utf-8"))

    chroma = chromadb.PersistentClient(path=DB_DIR)
    collection = chroma.get_or_create_collection(COLLECTION)

    total_chunks = 0
    indexed_files = 0

    for rel in changed:
        path = IMPORT_DIR / rel

        if not path.exists() or not path.is_file():
            continue

        if not allowed(path):
            continue

        text = read_file(path).strip()

        if not text:
            continue

        chunks = chunk_text(text)

        # delete old chunks for this file
        try:
            collection.delete(where={"source": rel})
        except Exception:
            pass

        for i, chunk in enumerate(chunks):
            chunk_id = hashlib.sha256(f"{rel}:{i}:{chunk}".encode()).hexdigest()

            collection.upsert(
                ids=[chunk_id],
                documents=[chunk],
                embeddings=[embed(chunk)],
                metadatas=[{
                    "source": rel,
                    "chunk": i,
                }]
            )

            total_chunks += 1

        indexed_files += 1
        print(f"indexed {rel}: {len(chunks)} chunks")

    print(f"done. indexed_files={indexed_files}, chunks={total_chunks}")

if __name__ == "__main__":
    main()
