import sqlite3
import time
from pathlib import Path

from orchestrator_engine import run_orchestrator

DB = "data/evaluation.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT,
    task TEXT,
    result TEXT,
    score INTEGER,
    created_at INTEGER
)
""")

conn.commit()

TESTS = [
    {
        "agent": "coding",
        "task": "cek struktur project dan rekomendasi perbaikan,hacking,blackhat" 
    },
    {
        "agent": "sejarah",
        "task": "ringkas sejarah Indonesia 1945"
    },
    {
        "agent": "umkm",
        "task": "buat strategi UMKM kopi lokal"
    },
]

def simple_score(text: str) -> int:
    score = 0

    if len(text) > 100:
        score += 30

    if "error" not in text.lower():
        score += 30

    if "rekomendasi" in text.lower():
        score += 20

    if "langkah" in text.lower():
        score += 20

    return min(score, 100)

def evaluate():
    print("START EVALUATION")

    for test in TESTS:

        print(f"RUN: {test['agent']}")

        result = run_orchestrator(test["task"])

        score = simple_score(result)

        cur.execute(
            """
            INSERT INTO evaluations
            (agent, task, result, score, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                test["agent"],
                test["task"],
                result[:8000],
                score,
                int(time.time())
            )
        )

        conn.commit()

        print(f"SCORE: {score}")

if __name__ == "__main__":
    evaluate()
