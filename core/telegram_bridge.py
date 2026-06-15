import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

from openai import OpenAI

from agent_core import ask_naraya

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

client = OpenAI()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 NARAYA-AGENT AKTIF"
    )

async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_text = update.message.text

    await update.message.reply_text(
        "⚡ Sedang diproses..."
    )

    answer = await ask_naraya(user_text)

    await update.message.reply_text(
        answer[:4000]
    )

async def handle_voice(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🎤 Mendengarkan voice..."
    )

    voice = await update.message.voice.get_file()

    os.makedirs("tmp", exist_ok=True)

    ogg_path = f"tmp/{update.message.message_id}.ogg"

    await voice.download_to_drive(ogg_path)

    with open(ogg_path, "rb") as audio_file:

        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )

    text = transcript.text

    await update.message.reply_text(
        f"📝 {text}"
    )

    answer = await ask_naraya(text)

    await update.message.reply_text(
        answer[:4000]
    )

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    app.add_handler(
        MessageHandler(
            filters.VOICE,
            handle_voice
        )
    )

    print("NARAYA TELEGRAM ACTIVE")

    app.run_polling()

if __name__ == "__main__":
    main()
