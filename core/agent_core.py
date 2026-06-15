import json
from openai import OpenAI
from rag_agent import master_agent, refresh_master_prompt
from agents import Runner

from memory_cache import (
    add_memory,
    get_recent_memory,
    get_cache,
    set_cache,
    add_knowledge,
    get_knowledge,
)

client = OpenAI()

def format_response_style(answer: str) -> str:
    answer = str(answer).strip()

    if answer.startswith("⚡ Dari cache:"):
        return answer

    style_prompt = f"""
Ubah jawaban berikut agar enak dibaca di Telegram.

Aturan:
- Bahasa Indonesia natural
- Tambahkan emoji secukupnya
- Paragraf pendek
- Gunakan bullet/numbering
- Jangan terlalu kaku
- Jangan ubah fakta utama
- Maksimal tetap ringkas

JAWABAN:
{answer}
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": style_prompt}
        ]
    )

    formatted = res.choices[0].message.content.strip()

    replacements = [
        ("**", ""),
        ("__", ""),
        ("##", ""),
        ("```", ""),
        ("`", ""),
    ]

    for a, b in replacements:
        formatted = formatted.replace(a, b)

    return formatted


def extract_knowledge_locally(message: str):
    text = message.strip()
    low = text.lower()

    rules = [
        ("goal", ["tujuan saya", "target saya", "saya ingin", "saya mau", "goal saya"]),
        ("project", ["project saya", "proyek saya", "nama project", "naraya-agent"]),
        ("preference", ["saya suka", "saya ingin jawaban", "gunakan gaya", "jangan"]),
        ("identity", ["nama saya", "saya adalah", "profesi saya"]),
        ("business", ["bisnis saya", "jualan", "produk saya"]),
    ]

    found = []

    for category, keywords in rules:
        if any(k in low for k in keywords):
            found.append({
                "category": category,
                "content": text,
                "confidence": 0.75
            })

    return found

async def auto_extract_knowledge(user_id: str, message: str):
    # Rule-based dulu: murah, hemat token
    items = extract_knowledge_locally(message)

    for item in items:
        add_knowledge(
            user_id=user_id,
            category=item["category"],
            content=item["content"],
            confidence=item["confidence"],
        )

async def ask_naraya(message: str, user_id: str = "default") -> str:
    cached = get_cache(user_id, message)

    if cached:
        return "⚡ Dari cache:\n\n" + cached

    await auto_extract_knowledge(user_id, message)

    memory = get_recent_memory(user_id)
    knowledge = get_knowledge(user_id)

    prompt = f"""
    MEMORY PERCAKAPAN TERAKHIR:
    {memory}

    PENGETAHUAN JANGKA PANJANG USER:
    {knowledge}

    PESAN USER:
    {message}

    Aturan:
    - jawab ringkas
    - hemat token
    - gunakan memory dan pengetahuan jangka panjang jika relevan
    - jangan tampilkan token, password, secret, credential, atau data pribadi sensitif
    """

    add_memory(user_id, "user", message)

    # pakai prompt aktif terbaru hasil evolusi pada setiap request
    refresh_master_prompt()

    result = await Runner.run(
        master_agent,
        prompt
    )

    answer = format_response_style(result.final_output)

    add_memory(user_id, "assistant", answer)
    set_cache(user_id, message, answer)

    return answer


# Alias kompatibilitas untuk pemanggil lama (backend/frontend/integrasi)
ask_nusantara = ask_naraya


def work(goal: str, mode: str = "parallel", revise: bool = True, on_event=None) -> str:
    """Kerjakan sebuah pekerjaan SELALU lewat orkestrasi multi-agen (14 agen spesialis).
    mode: 'parallel' (default) atau 'sequential'. revise: loop perbaikan otomatis.
    on_event(ev): callback streaming progress tiap agen."""
    import multi_agent
    return multi_agent.work(goal, mode, revise, on_event)
