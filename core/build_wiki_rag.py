import json
import hashlib
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

RAW = Path("data/wiki_raw")
DB_DIR = "data/chroma_db"
COLLECTION = "wiki_knowledge"

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

def chunk_text(text, max_chars=2500, overlap=250):
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start = end - overlap

    return chunks

def embed(text):
    return model.encode(text).tolist()

def main():
    chroma = chromadb.PersistentClient(path=DB_DIR)
    col = chroma.get_or_create_collection(COLLECTION)

    total = 0

    for file in RAW.glob("*.json"):
        data = json.loads(file.read_text(encoding="utf-8"))

        text = f"""
{data.get("title","")}

{data.get("summary","")}

{data.get("text","")}
"""

        chunks = chunk_text(text)

        for i, ch in enumerate(chunks):
            cid = hashlib.sha256(
                f"{file.name}:{i}:{ch}".encode()
            ).hexdigest()

            col.upsert(
                ids=[cid],
                documents=[ch],
                embeddings=[embed(ch)],
                metadatas=[{
                    "source": "wikipedia",
                    "title": data.get("title",""),
                    "url": data.get("url",""),
                    "chunk": i
                }]
            )

            total += 1

        print("INDEXED:", data.get("title"), len(chunks))

    print("DONE chunks:", total)

if __name__ == "__main__":
    main()
