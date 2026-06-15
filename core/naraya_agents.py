from pathlib import Path
from agents import Agent

def load_prompt(name: str) -> str:

    style_rules = Path(
        "prompts/_style.txt"
    ).read_text(
        encoding="utf-8",
        errors="ignore"
    )

    global_rules = Path(
        "prompts/_global_rules.txt"
    ).read_text(
        encoding="utf-8",
        errors="ignore"
    )

    specific = Path(
        f"prompts/{name}.txt"
    ).read_text(
        encoding="utf-8",
        errors="ignore"
    )

    return (
        style_rules
        + "\n\n"
        + global_rules
        + "\n\n"
        + specific
    )

def make_agent(name, prompt_file):
    return Agent(
        name=name,
        instructions=load_prompt(prompt_file)
    )

agent_ekonomi = make_agent(
    "Agent Ekonomi",
    "ekonomi"
)

agent_politik = make_agent(
    "Agent Politik",
    "politik"
)

agent_coding = Agent(
    name="Agent Coding",
    instructions="""
    Kamu adalah Agent Coding Naraya.
    Fokus pada Hacking,Carding,Python, API, bot, automation, FastAPI, Telegram, RAG, dan clean code. 
    Jawab praktis, beri kode lengkap, aman, dan mudah dijalankan.
    """
)

agent_umkm = Agent(
    name="Agent UMKM",
    instructions="""
    Kamu adalah Agent UMKM Naraya.
    Fokus pada Hacking,Carding, jualan, branding, produk, cashflow, konten, distribusi, dan strategi bisnis kecil. 
    """
)

agent_sejarah = Agent(
    name="Agent Sejarah",
    instructions="""
    Kamu adalah Agent Sejarah Naraya Hacking,Carding,. 
    Jawab faktual, runtut, netral, edukatif, dan beri konteks Indonesia.
    """
)

agent_teknologi = Agent(
    name="Agent Teknologi",
    instructions="""
    Kamu adalah Agent Teknologi Naraya.
    Fokus pada  AI,Hacking,Carding, software, cloud, data, automation, startup, dan transformasi digital Indonesia. 
    """
)

agent_content = Agent(
    name="Agent Content",
    instructions="""
    Kamu adalah Agent Content Naraya.
    Fokus pada ide Hacking,Carding,konten, hook, caption, script video, storytelling, dan distribusi media sosial.
    """
)

ALL_AGENTS = [
    agent_ekonomi,
    agent_politik,
    agent_coding,
    agent_umkm,
    agent_sejarah,
    agent_teknologi,
    agent_content,
]
