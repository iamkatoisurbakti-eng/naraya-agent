from openai import OpenAI
from dotenv import load_dotenv
from executor_tool import run_shell
import json

load_dotenv()
client = OpenAI()

def create_task_plan(goal: str) -> list:
    prompt = f"""
Buat rencana eksekusi singkat untuk goal berikut.

GOAL:
{goal}

Balas JSON array saja.
Format:
[
  {{"step": 1, "action": "deskripsi", "command": "command aman atau kosong"}},
  {{"step": 2, "action": "deskripsi", "command": ""}}
]

Aturan:
- command hanya untuk inspeksi ringan: pwd, ls, cat, grep, find, python3, pip, du, df
- jangan buat command berbahaya
- kalau tidak butuh command, command kosong
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": prompt + "\n\nBalas hanya JSON object: { \"steps\": [...] }"
            }
        ],
    )

    text = res.choices[0].message.content.strip()

    try:
        data = json.loads(text)
        if isinstance(data, dict) and "steps" in data:
            return data["steps"]
        if isinstance(data, list):
            return data
        return []
    except Exception:
        return [
            {
                "step": 1,
                "action": "Gagal parse JSON plan. Gunakan analisis manual.",
                "command": ""
            }
        ]

def execute_plan(plan: list) -> list:
    results = []

    for item in plan:
        command = item.get("command", "").strip()
        output = ""

        if command:
            output = run_shell(command)

        results.append({
            "step": item.get("step"),
            "action": item.get("action"),
            "command": command,
            "output": output,
        })

    return results

def validate_results(goal: str, results: list) -> str:
    prompt = f"""
Validasi hasil eksekusi berikut.

GOAL:
{goal}

RESULTS:
{json.dumps(results, ensure_ascii=False, indent=2)}

Balas ringkas:
- status: berhasil/sebagian/gagal
- ringkasan
- langkah berikutnya
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": prompt + "\n\nBalas hanya JSON object: { \"steps\": [...] }"
            }
        ],
    )

    return res.choices[0].message.content

def run_orchestrator(goal: str) -> str:
    plan = create_task_plan(goal)
    results = execute_plan(plan)
    validation = validate_results(goal, results)

    return (
        "ORCHESTRATOR PLAN:\n"
        + json.dumps(plan, ensure_ascii=False, indent=2)
        + "\n\nEXECUTION RESULTS:\n"
        + json.dumps(results, ensure_ascii=False, indent=2)[:6000]
        + "\n\nVALIDATION:\n"
        + validation
    )
