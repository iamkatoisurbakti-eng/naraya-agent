from openai import OpenAI
from dotenv import load_dotenv
import subprocess

load_dotenv()

client = OpenAI()

def run_python(file_path: str):

    try:

        result = subprocess.run(
            ["python3", file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "ok": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {
            "ok": False,
            "stderr": str(e)
        }

def repair_code(code: str, error: str):

    prompt = f"""
Perbaiki kode Python berikut.

ERROR:
{error}

CODE:
{code}

Balas hanya kode final.
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return res.choices[0].message.content
