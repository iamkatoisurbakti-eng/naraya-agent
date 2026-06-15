import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

def embed(text):
    return model.encode(text).tolist()

def search_wiki(query, n=5):
    try:
        chroma = chromadb.PersistentClient(path="data/chroma_db")
        col = chroma.get_or_create_collection("wiki_knowledge")

        if col.count() == 0:
            return [{
                "title": "Wikipedia belum terindex",
                "url": "",
                "text": "Jalankan: python3 build_wiki_rag.py"
            }]

        q = embed(query)

        res = col.query(
            query_embeddings=[q],
            n_results=n
        )

        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]

        out = []

        for doc, meta in zip(docs, metas):
            out.append({
                "title": meta.get("title"),
                "url": meta.get("url"),
                "text": doc[:1200]
            })

        return out

    except Exception as e:
        return [{
            "title": "Wiki search error",
            "url": "",
            "text": str(e)
        }]
