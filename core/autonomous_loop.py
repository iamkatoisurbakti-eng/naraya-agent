import json
import time
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("/root/naraya-agent/.env")

client = OpenAI()

TASKS = json.load(
    open("benchmarks/tasks.json")
)

LOG = Path("logs/autonomous/loop.log")

MAX_TASKS = 3

def log(msg):

    LOG.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    line = f"[{int(time.time())}] {msg}"

    print(line)

    with LOG.open("a") as f:
        f.write(line + "\n")

def ask(prompt):

    r = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return r.choices[0].message.content

def evaluate(task, answer):

    eval_prompt = f"""
Nilai jawaban berikut dari 1-10.

TASK:
{task}

ANSWER:
{answer}

Berikan:
- score
- weakness
- improvement
"""

    return ask(eval_prompt)

def main():

    log("=== AUTONOMOUS LOOP START ===")

    for task in TASKS[:MAX_TASKS]:

        prompt = task["task"]

        log(f"RUN TASK: {prompt}")

        answer = ask(prompt)

        score = evaluate(
            prompt,
            answer
        )

        log(f"ANSWER: {answer[:500]}")
        log(f"EVAL: {score[:500]}")

        time.sleep(10)

    log("=== LOOP DONE ===")

if __name__ == "__main__":
    main()
