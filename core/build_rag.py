from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
import hashlib

load_dotenv()

client = OpenAI()

DATA_FILE = Path("data/hermes_knowledge.md")

DB_DIR = "data/chroma_db"
COLLECTION = "hermes_knowledge"

def chunk_text(text, max_chars=3000, overlap=300):

    chunks = []
    start = 0

    while start < len(text):

        end = start + max_chars
        chunk = text[start:end]

        chunks.append(chunk)

        start = end - overlap

    return chunks

def embed(text):

    result = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return result.data[0].embedding

def main():

    text = DATA_FILE.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    chunks = chunk_text(text)

    chroma = chromadb.PersistentClient(path=DB_DIR)

    collection = chroma.get_or_create_collection(
        COLLECTION
    )

    print("TOTAL CHUNKS:", len(chunks))

    for i, chunk in enumerate(chunks):

        chunk_id = hashlib.md5(
            chunk.encode("utf-8")
        ).hexdigest()

        collection.upsert(
            ids=[chunk_id],
            documents=[chunk],
            embeddings=[embed(chunk)],
            metadatas=[{
                "chunk": i
            }]
        )

        if i % 10 == 0:
            print("INDEX:", i)

    print("SELESAI")

if __name__ == "__main__":
    main()
