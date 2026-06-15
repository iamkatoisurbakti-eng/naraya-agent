from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def generate_dataset(topic: str, amount: int = 10):

    prompt = f"""
Buat dataset sintetik tentang:
{topic}

Jumlah:
{amount}

Format JSON array:
[
  {{
    "question": "...",
    "answer": "..."
  }}
]
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
