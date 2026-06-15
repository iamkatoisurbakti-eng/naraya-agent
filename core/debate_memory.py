import sqlite3
import time

conn = sqlite3.connect("data/naraya_memory.db")
cur = conn.cursor()

def save_debate_knowledge(topic, synthesis):

    cur.execute("""
    INSERT INTO long_term_knowledge
    (
        user_id,
        category,
        content,
        confidence,
        created_at
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        "system",
        "debate_insight",
        f"{topic}\n\n{synthesis}",
        0.85,
        int(time.time())
    ))

    conn.commit()
