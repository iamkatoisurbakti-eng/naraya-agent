import sqlite3

conn = sqlite3.connect("data/evolution.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS evolution_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    component TEXT,
    old_version TEXT,
    new_version TEXT,
    score_before REAL,
    score_after REAL,
    improvement REAL,
    applied INTEGER,
    created_at INTEGER
)
""")

conn.commit()

def save_evolution(
    component,
    old_version,
    new_version,
    score_before,
    score_after,
    applied
):

    improvement = score_after - score_before

    cur.execute(
        """
        INSERT INTO evolution_history
        (
            component,
            old_version,
            new_version,
            score_before,
            score_after,
            improvement,
            applied,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, strftime('%s','now'))
        """,
        (
            component,
            old_version,
            new_version,
            score_before,
            score_after,
            improvement,
            applied
        )
    )

    conn.commit()
