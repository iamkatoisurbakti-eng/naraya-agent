from pathlib import Path
from agent_core import ask_naraya
import asyncio
import time

HTML_FILE = Path("/root/naraya-agent/aspri-x-naraya-v2.html")
OUT_DIR = Path("data/app-analysis")
OUT_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    html = HTML_FILE.read_text(encoding="utf-8", errors="ignore")

    prompt = f"""
    Evaluasi aplikasi HTML berikut sebagai produk digital.

    Tugas:
    1. Ringkas fungsi aplikasi
    2. Deteksi modul utama
    3. Evaluasi UI/UX
    4. Evaluasi route yang perlu disambungkan ke Naraya-Agent
    5. Buat roadmap integrasi backend
    6. Buat daftar skill/knowledge yang harus dipelajari agent
    7. Beri rekomendasi prioritas 7 hari

    HTML:
    {html[:60000]}
    """

    result = await ask_naraya(prompt, user_id="app-evaluator")

    out = OUT_DIR / f"analysis_{int(time.time())}.md"
    out.write_text(result, encoding="utf-8")

    print("OK:", out)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
