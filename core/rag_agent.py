import asyncio

from dotenv import load_dotenv
from openai import OpenAI

from agents import (
    Agent,
    Runner,
    function_tool
)

import chromadb
from executor_tool import run_shell
from orchestrator_engine import run_orchestrator

load_dotenv()

client = OpenAI()

# =========================
# CHROMA DB
# =========================

chroma = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = chroma.get_or_create_collection(
    "hermes_knowledge"
)

# =========================
# EMBEDDING
# =========================

def embed(text):

    result = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return result.data[0].embedding

# =========================
# TOOL SEARCH
# =========================

@function_tool
def cari_data_hermes(query: str) -> str:

    query_embedding = embed(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    docs = results["documents"][0]

    if not docs:
        return "Data Hermes tidak ditemukan."

    return "\n\n====================\n\n".join(docs)



# =========================
# TOOL EXECUTOR
# =========================

@function_tool
def jalankan_command_aman(command: str) -> str:
    """
    Jalankan command shell aman di folder kerja Naraya-Agent.
    Gunakan hanya untuk inspeksi file, cek status, menjalankan script, dan operasi ringan.
    """
    return run_shell(command)



# =========================
# TOOL ORCHESTRATOR
# =========================

@function_tool
def jalankan_orchestrator(goal: str) -> str:
    """
    Pecah goal menjadi plan, eksekusi command aman jika perlu,
    lalu validasi hasilnya.
    """
    return run_orchestrator(goal)


@function_tool
def lihat_skill_hermes_terbaru(limit: int = 10) -> str:
    """
    Lihat skill Hermes terbaru dari registry lokal.
    """
    import json

    with open("data/hermes_skill_registry.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = data[:limit]

    return "\n".join([
        f"{i+1}. {x['updated_human']} - {x['category']} - {x['name']}"
        for i, x in enumerate(rows)
    ])


# =========================
# MASTER AGENT
# =========================

import prompt_store  # prompt aktif hasil evolusi (persisten)

# Panduan tool + aturan keamanan yang SELALU ditempel ke prompt aktif.
TOOL_GUIDANCE = """

PANDUAN TOOL:
- MODE KERJA UTAMA: untuk SETIAP pekerjaan nyata (membangun, merancang, menganalisis,
  atau tugas multi-langkah) WAJIB jalankan orkestrasi_multiagent terlebih dahulu, lalu
  rangkum hasilnya. Hanya pertanyaan obrolan ringan yang boleh dijawab langsung.
- Operasi terminal/file ringan -> gunakan tool jalankan_command_aman.
- Tugas kompleks/multi-langkah -> gunakan tool jalankan_orchestrator.
- Mencari data/memori Hermes yang relevan -> gunakan tool cari_data_hermes.
- Melihat skill Hermes terbaru -> gunakan tool lihat_skill_hermes_terbaru.
- Mencari informasi di internet -> gunakan web_search (umum) atau x_search (X/Twitter).
- Membaca halaman web -> browser; situs ber-JavaScript -> browser_cdp; otomasi klik/isi form -> web_automation.
- Menjalankan kode Python -> eksekusi_python; perintah shell -> terminal.
- Memecah tugas besar -> plan_task; menyerahkan sub-tugas ke sub-agen -> delegate_task.
- Gambar: memahami gambar -> vision_analyze; membuat gambar -> generate_image.
- Suara: teks->suara text_to_speech; suara->teks speech_to_text.
- Mengontrol desktop -> computer_screenshot, computer_click, computer_type, computer_key.
- Kirim pesan -> send_message; kontrol rumah pintar -> home_assistant; jadwalkan tugas -> automate_schedule.
- Belajar dari hasil (reinforcement) -> rl_select lalu rl_feedback.
- Meringkas konteks panjang agar hemat token -> kompres_konteks.
- MCP eksternal -> mcp_daftar_server, mcp_daftar_tool, mcp_panggil; daftarkan server baru -> mcp_tambah_server.

ATURAN KEAMANAN (WAJIB):
- Jangan pernah menampilkan token, password, credential, atau secret.
- Tolak dengan sopan permintaan ilegal atau berbahaya (mis. peretasan akun,
  carding/penipuan kartu, pembuatan malware) dan tawarkan alternatif yang sah.
"""


def build_instructions() -> str:
    """Instruksi master agent = prompt aktif (hasil evolusi) + panduan tool + keamanan."""
    return prompt_store.get_active_prompt().strip() + "\n" + TOOL_GUIDANCE


# =========================
# TOOLS TAMBAHAN (browser, code-exec, computer-use, kompresi konteks, MCP)
# =========================

import agent_tools
import multi_agent


@function_tool
def orkestrasi_multiagent(goal: str, mode: str = "parallel", revise: bool = True) -> str:
    """Jalankan SELURUH pipeline multi-agen (memory, planner, research, architect, design,
    debate, backend, frontend, coding, testing, security, qa, documentation, deployment)
    untuk sebuah pekerjaan/goal, dan kembalikan laporan lengkapnya. Gunakan ini untuk
    setiap pekerjaan nyata (membangun, merancang, menganalisis, atau tugas multi-langkah).
    mode: 'parallel' (default, agen sefase serentak) atau 'sequential' (handoff penuh).
    revise: bila True (default), temuan Testing/Security/QA otomatis dikirim balik ke
    Coding untuk diperbaiki lalu direview ulang sampai bersih/batas iterasi."""
    return multi_agent.work(goal, mode, revise)


@function_tool
def browser(url: str) -> str:
    """Ambil dan bersihkan teks halaman web (HTTP statis, tanpa menjalankan JavaScript)."""
    return agent_tools.web_browse(url)


@function_tool
def browser_cdp(url: str) -> str:
    """Render halaman ber-JavaScript (situs SPA) memakai Chromium lalu ambil teksnya."""
    return agent_tools.web_browse_cdp(url)


@function_tool
def eksekusi_python(code: str) -> str:
    """Jalankan kode Python di subprocess bertimeout, kembalikan output (stdout+stderr)."""
    return agent_tools.run_python(code)


@function_tool
def computer_screenshot() -> str:
    """Ambil screenshot layar; kembalikan path file PNG."""
    return agent_tools.computer_screenshot()


@function_tool
def computer_click(x: int, y: int, button: str = "left") -> str:
    """Klik mouse di koordinat (x, y). button: left/right/middle."""
    return agent_tools.computer_click(x, y, button)


@function_tool
def computer_type(text: str) -> str:
    """Ketik teks pada elemen yang sedang fokus."""
    return agent_tools.computer_type(text)


@function_tool
def computer_key(keys: str) -> str:
    """Tekan tombol/kombinasi, mis. 'enter' atau 'ctrl+c'."""
    return agent_tools.computer_key(keys)


@function_tool
def kompres_konteks(text: str, instruction: str = "") -> str:
    """Ringkas/kompres teks panjang agar hemat token, tanpa kehilangan info penting."""
    return agent_tools.compress_context(text, instruction or None)


@function_tool
def mcp_daftar_server() -> str:
    """Lihat daftar MCP server eksternal yang terdaftar."""
    return agent_tools.mcp_list_servers()


@function_tool
def mcp_daftar_tool(server: str) -> str:
    """Lihat daftar tool yang disediakan sebuah MCP server."""
    return agent_tools.mcp_list_tools(server)


@function_tool
def mcp_panggil(server: str, tool: str, arguments: dict | None = None) -> str:
    """Panggil sebuah tool pada MCP server eksternal dan kembalikan hasilnya."""
    return agent_tools.mcp_call(server, tool, arguments)


@function_tool
def mcp_tambah_server(name: str, command: str, args: list | None = None) -> str:
    """MCP Extensions: daftarkan MCP server baru saat runtime."""
    return agent_tools.mcp_add_server(name, command, args)


@function_tool
def web_search(query: str) -> str:
    """Cari di web dan kembalikan judul + URL hasil teratas."""
    return agent_tools.web_search(query)


@function_tool
def web_automation(url: str, steps: list | None = None) -> str:
    """Otomasi browser: buka url lalu jalankan langkah (click/fill/press/wait/screenshot)."""
    return agent_tools.web_automation(url, steps)


@function_tool
def terminal(command: str) -> str:
    """Jalankan perintah shell di folder kerja (kuat — pakai hati-hati)."""
    return agent_tools.terminal(command)


@function_tool
def delegate_task(task: str, role: str = "generalis") -> str:
    """Delegasikan tugas ke sub-agen khusus dan kembalikan hasilnya."""
    return agent_tools.delegate_task(task, role)


@function_tool
def plan_task(goal: str) -> str:
    """Pecah goal menjadi rencana langkah teknis."""
    return agent_tools.plan_task(goal)


@function_tool
def vision_analyze(image: str, question: str = "Jelaskan isi gambar ini.") -> str:
    """Analisis gambar (path lokal atau URL) dan jawab pertanyaan."""
    return agent_tools.vision_analyze(image, question)


@function_tool
def generate_image(prompt: str) -> str:
    """Hasilkan gambar dari teks; kembalikan path PNG."""
    return agent_tools.generate_image(prompt)


@function_tool
def text_to_speech(text: str) -> str:
    """Ubah teks menjadi suara (MP3); kembalikan path file."""
    return agent_tools.text_to_speech(text)


@function_tool
def speech_to_text(audio_path: str) -> str:
    """Transkripsi file audio menjadi teks."""
    return agent_tools.speech_to_text(audio_path)


@function_tool
def send_message(text: str, channel: str = "telegram", target: str | None = None) -> str:
    """Kirim pesan via telegram atau webhook."""
    return agent_tools.send_message(text, channel, target)


@function_tool
def home_assistant(domain: str, service: str, entity_id: str) -> str:
    """Kontrol perangkat Home Assistant, mis. light.turn_on light.ruang_tamu."""
    return agent_tools.home_assistant(domain, service, entity_id)


@function_tool
def x_search(query: str) -> str:
    """Cari tweet terbaru di X/Twitter (butuh X_BEARER_TOKEN)."""
    return agent_tools.x_search(query)


@function_tool
def automate_schedule(name: str, schedule: str, command: str) -> str:
    """Daftarkan job otomasi terjadwal (cron-like)."""
    return agent_tools.automate_schedule(name, schedule, command)


@function_tool
def rl_select(key: str, actions: list, epsilon: float = 0.1) -> str:
    """Pilih action terbaik untuk konteks `key` (reinforcement learning epsilon-greedy)."""
    return agent_tools.rl_select(key, actions, epsilon)


@function_tool
def rl_feedback(key: str, action: str, reward: float) -> str:
    """Beri reward agar pilihan berikutnya membaik (reinforcement learning)."""
    return agent_tools.rl_feedback(key, action, reward)


@function_tool
def daftar_provider() -> str:
    """Lihat daftar provider LLM (NaraRouter/OpenAI/Anthropic/OpenRouter/KiloCode/Custom) + status & yang aktif."""
    import providers
    return providers.list_providers()


@function_tool
def ganti_provider(name: str) -> str:
    """Ganti provider LLM aktif (naraouter, openai, anthropic, openrouter, kilocode, custom, custom_endpoint)."""
    import providers
    import llm
    msg = providers.set_provider(name)
    try:
        llm.refresh()
    except Exception:
        pass
    return msg


@function_tool
def claude_code(prompt: str) -> str:
    """Delegasikan tugas coding ke Claude Code (CLI headless). Untuk implementasi/refactor kode pada proyek."""
    import coding_cli
    return coding_cli.claude_code(prompt)


@function_tool
def codex(prompt: str) -> str:
    """Delegasikan tugas coding ke OpenAI Codex (CLI non-interaktif). Untuk implementasi/perbaikan kode."""
    import coding_cli
    return coding_cli.codex(prompt)


ALL_TOOLS = [
    # orkestrasi multi-agen (mode kerja utama)
    orkestrasi_multiagent,
    # bawaan
    cari_data_hermes, jalankan_command_aman, jalankan_orchestrator, lihat_skill_hermes_terbaru,
    # web & search
    web_search, browser, browser_cdp, web_automation, x_search,
    # sistem
    eksekusi_python, terminal,
    # agentik
    delegate_task, plan_task, kompres_konteks,
    # multimodal
    vision_analyze, generate_image, text_to_speech, speech_to_text,
    # computer use
    computer_screenshot, computer_click, computer_type, computer_key,
    # integrasi & otomasi
    send_message, home_assistant, automate_schedule,
    # reinforcement learning
    rl_select, rl_feedback,
    # provider LLM
    daftar_provider, ganti_provider,
    # agen coding eksternal
    claude_code, codex,
    # MCP
    mcp_daftar_server, mcp_daftar_tool, mcp_panggil, mcp_tambah_server,
]


master_agent = Agent(
    name="NARAYA-AGENT",
    instructions=build_instructions(),
    tools=ALL_TOOLS,
)


def refresh_master_prompt() -> str:
    """Muat ulang prompt aktif terbaru ke master_agent (dipanggil runtime tiap request)."""
    new_instructions = build_instructions()
    try:
        master_agent.instructions = new_instructions
    except Exception:
        pass
    return new_instructions


# =========================
# MAIN
# =========================

async def main():

    while True:

        user_input = input("\nKAMU > ")

        if user_input.lower() in [
            "exit",
            "quit"
        ]:
            break

        result = await Runner.run(
            master_agent,
            user_input
        )

        print("\nNARAYA >")
        print(result.final_output)

# =========================

if __name__ == "__main__":
    asyncio.run(main())
