import sqlite3

conn = sqlite3.connect("data/naraya_memory.db")
cur = conn.cursor()

def refine():

    cur.execute("""
    SELECT content
    FROM memories
    ORDER BY id DESC
    LIMIT 100
    """)

    rows = cur.fetchall()

    combined = "\n".join([
        r[0]
        for r in rows
    ])

    summary = combined[:4000]

    cur.execute("""
    INSERT INTO long_term_knowledge
    (user_id, category, content, confidence, created_at)
    VALUES (?, ?, ?, ?, strftime('%s','now'))
    """, (
        "system",
        "memory_summary",
        summary,
        0.8
    ))

    conn.commit()

if __name__ == "__main__":
    refine()
