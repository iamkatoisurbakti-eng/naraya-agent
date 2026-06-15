from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def create_plan(goal: str):

    prompt = f"""
    Pecah goal berikut menjadi langkah teknis.

    Goal:
    {goal}

    Format:
    1.
    2.
    3.
    """

    result = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return result.choices[0].message.content
