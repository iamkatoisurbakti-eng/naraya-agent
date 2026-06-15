from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def synthesize(topic, debate_result):

    prompt = f"""
Lakukan sintesis dari debat berikut.

TOPIK:
{topic}

DEBAT:
{debate_result}

Tugas:
1. gabungkan insight terbaik
2. cari titik temu
3. buat rekomendasi final
4. buat pelajaran strategis
5. buat praktek

Format:
- Insight utama
- Risiko
- Strategi
- Kesimpulan
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
