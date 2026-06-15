import sqlite3

conn = sqlite3.connect("data/evaluation.db")
cur = conn.cursor()

cur.execute("""
SELECT agent, AVG(score)
FROM evaluations
GROUP BY agent
ORDER BY AVG(score) DESC
""")

rows = cur.fetchall()

print("\nNARAYA LEADERBOARD\n")

for r in rows:
    print(f"{r[0]}: {round(r[1],2)}")
