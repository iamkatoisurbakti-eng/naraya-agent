import sqlite3
from pathlib import Path

def check():
    result = {}

    result["project_dir"] = Path(".").resolve().as_posix()
    result["data_exists"] = Path("data").exists()
    result["chroma_exists"] = Path("data/chroma_db").exists()
    result["memory_db_exists"] = Path("data/naraya_memory.db").exists()
    result["logs_exists"] = Path("logs").exists()

    if Path("data/naraya_memory.db").exists():
        conn = sqlite3.connect("data/naraya_memory.db")
        cur = conn.cursor()

        for table in ["memories", "response_cache", "long_term_knowledge"]:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                result[table] = cur.fetchone()[0]
            except Exception as e:
                result[table] = f"ERROR: {e}"

        conn.close()

    return result

if __name__ == "__main__":
    for k, v in check().items():
        print(f"{k}: {v}")
