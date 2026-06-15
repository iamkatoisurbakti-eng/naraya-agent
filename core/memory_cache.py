import sqlite3
import hashlib
import time
import json
from pathlib import Path

DB_PATH = Path("data/naraya_memory.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    role TEXT,
    content TEXT,
    created_at INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS response_cache (
    key TEXT PRIMARY KEY,
    prompt TEXT,
    response TEXT,
    created_at INTEGER
)
""")

conn.commit()

def safe_text(text: str) -> str:
    text = str(text)
    blocked = ["sk-proj-", "sk-", "api_key", "password=", "secret=", "credential=", "authorization:", "bearer "]
    lowered = text.lower()

    if any(x in lowered for x in blocked):
        return "[DATA SENSITIF DIHAPUS]"

    return text[:4000]

def write_knowledge_log(user_id: str, role: str, content: str):
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    record = {
        "time": int(time.time()),
        "user_id": user_id,
        "role": role,
        "content": safe_text(content),
    }

    with (log_dir / "knowledge.log").open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def add_memory(user_id: str, role: str, content: str):
    cur.execute(
        """
        INSERT INTO memories (user_id, role, content, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, role, safe_text(content), int(time.time()))
    )
    conn.commit()
    write_knowledge_log(user_id, role, content)

def get_recent_memory(user_id: str, limit: int = 8) -> str:
    cur.execute(
        """
        SELECT role, content FROM memories
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    )

    rows = cur.fetchall()[::-1]

    if not rows:
        return ""

    return "\n".join([f"{role}: {content}" for role, content in rows])

def make_cache_key(user_id: str, prompt: str) -> str:
    raw = f"{user_id}:{prompt.strip().lower()}"
    return hashlib.sha256(raw.encode()).hexdigest()

def get_cache(user_id: str, prompt: str):
    key = make_cache_key(user_id, prompt)

    cur.execute(
        "SELECT response FROM response_cache WHERE key = ?",
        (key,)
    )

    row = cur.fetchone()
    return row[0] if row else None

def set_cache(user_id: str, prompt: str, response: str):
    key = make_cache_key(user_id, prompt)

    cur.execute(
        """
        INSERT OR REPLACE INTO response_cache
        (key, prompt, response, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (key, safe_text(prompt), safe_text(response), int(time.time()))
    )

    conn.commit()

# =========================================
# LONG TERM KNOWLEDGE
# =========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS long_term_knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    category TEXT,
    content TEXT,
    confidence REAL,
    created_at INTEGER
)
""")

conn.commit()

def add_knowledge(user_id: str, category: str, content: str, confidence: float = 0.8):
    content = safe_text(content)

    if not content or content == "[DATA SENSITIF DIHAPUS]":
        return

    cur.execute(
        """
        INSERT INTO long_term_knowledge
        (user_id, category, content, confidence, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, category, content, confidence, int(time.time()))
    )

    conn.commit()
    write_knowledge_log(user_id, "knowledge", f"{category}: {content}")

def get_knowledge(user_id: str, limit: int = 10) -> str:
    cur.execute(
        """
        SELECT category, content FROM long_term_knowledge
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    )

    rows = cur.fetchall()[::-1]

    if not rows:
        return ""

    return "\n".join([f"- {cat}: {content}" for cat, content in rows])


def replace_knowledge(
    user_id: str,
    category: str,
    content: str,
    confidence: float = 0.9
):

    cur.execute(
        """
        DELETE FROM long_term_knowledge
        WHERE user_id = ?
        AND category = ?
        """,
        (user_id, category)
    )

    conn.commit()

    add_knowledge(
        user_id=user_id,
        category=category,
        content=content,
        confidence=confidence
    )

def replace_knowledge(user_id: str, category: str, content: str, confidence: float = 0.9):
    cur.execute(
        """
        DELETE FROM long_term_knowledge
        WHERE user_id = ?
        AND category = ?
        """,
        (user_id, category)
    )
    conn.commit()

    add_knowledge(
        user_id=user_id,
        category=category,
        content=content,
        confidence=confidence
    )
