from synthesis_engine import synthesize
from debate_memory import save_debate_knowledge
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def ask_agent(role: str, topic: str):

    prompt = f"""
Anda adalah agent:
{role}

Bahas topik:
{topic}

Jawab singkat dan kuat.
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

def debate(topic: str):

    politik = ask_agent(
        "Agent Politik",
        topic
    )

    ekonomi = ask_agent(
        "Agent Ekonomi",
        topic
    )

    validator = ask_agent(
        "Agent Validator",
        f"""
POLITIK:
{politik}

EKONOMI:
{ekonomi}

Siapa lebih kuat?
Apa kelemahannya?
"""
    )

    debate_result = f"""
=== POLITIK ===
{politik}

=== EKONOMI ===
{ekonomi}

=== VALIDATOR ===
{validator}
"""

    synthesis = synthesize(
        topic,
        debate_result
    )

    save_debate_knowledge(
        topic,
        synthesis
    )

    return debate_result + f"""

=== SYNTHESIS ===
{synthesis}
"""
