"""
gateway.py — Jalankan Naraya di platform pesan (gaya Hermes gateway).

Telegram didukung penuh (long-polling Bot API, tanpa dependensi tambahan selain
httpx/urllib yang sudah dipakai). Platform lain (WhatsApp/Discord/Slack) tersedia
sebagai stub yang menjelaskan cara mengaktifkan.

Env: TELEGRAM_BOT_TOKEN (wajib), TELEGRAM_ALLOWED_USERS (csv id, opsional),
     NARAYA_GATEWAY_ALLOW_ALL=true (izinkan semua user — hati-hati).

Pesan biasa -> dijawab agen (llm + prompt aktif + memori per-chat).
'/work <goal>' -> orkestrasi multi-agen penuh.
"""

from __future__ import annotations

import os
import json
import time


def _reply(text: str, chat_id) -> str:
    text = (text or "").strip()
    if text in ("/start", "/help"):
        return ("Halo! Saya Naraya 🇮🇩. Kirim pesan untuk ngobrol, atau:\n"
                "• /work <tugas> — orkestrasi multi-agen\n• /help — bantuan")
    if text.startswith("/work"):
        goal = text[5:].strip()
        if not goal:
            return "Pakai: /work <deskripsi tugas>"
        try:
            import multi_agent
            return multi_agent.work(goal)
        except Exception as exc:
            return f"[error work] {exc}"
    try:
        import llm
        import prompt_store
    except Exception as exc:
        return f"[error] modul tidak siap: {exc}"
    if not llm.is_available():
        return "Provider/API key belum diset di .env."
    mem = ""
    add_memory = None
    try:
        from memory_cache import add_memory as _am, get_recent_memory
        add_memory = _am
        mem = get_recent_memory(f"tg:{chat_id}")
    except Exception:
        pass
    prompt = f"Memori:\n{mem}\n\nPesan: {text}" if mem else text
    try:
        ans = llm.chat(prompt, system=prompt_store.get_active_prompt())
    except Exception as exc:
        ans = f"[error] {exc}"
    if add_memory:
        try:
            add_memory(f"tg:{chat_id}", "user", text)
            add_memory(f"tg:{chat_id}", "assistant", ans)
        except Exception:
            pass
    return ans


def telegram(poll_timeout: int = 30) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Set TELEGRAM_BOT_TOKEN di .env dulu.")
        return
    allowed = {x for x in os.getenv("TELEGRAM_ALLOWED_USERS", "").replace(" ", "").split(",") if x}
    allow_all = os.getenv("NARAYA_GATEWAY_ALLOW_ALL", "").lower() == "true"
    import agent_tools
    api = f"https://api.telegram.org/bot{token}"
    offset = None
    print("Naraya Telegram gateway aktif. Ctrl+C untuk berhenti.")
    while True:
        try:
            params = {"timeout": poll_timeout}
            if offset:
                params["offset"] = offset
            _, body = agent_tools._http_get(f"{api}/getUpdates", params=params, timeout=poll_timeout + 10)
            data = json.loads(body)
            for upd in data.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message") or upd.get("edited_message")
                if not msg or "text" not in msg:
                    continue
                chat_id = msg["chat"]["id"]
                uid = str(msg.get("from", {}).get("id", ""))
                text = msg["text"]
                if not allow_all and allowed and uid not in allowed:
                    agent_tools._http_post(f"{api}/sendMessage",
                                           json_body={"chat_id": chat_id, "text": "Maaf, kamu tidak diizinkan."})
                    continue
                reply = _reply(text, chat_id)
                for i in range(0, len(reply) or 1, 3900):  # patuhi limit 4096
                    agent_tools._http_post(f"{api}/sendMessage",
                                           json_body={"chat_id": chat_id, "text": reply[i:i + 3900] or "(kosong)"})
        except KeyboardInterrupt:
            print("\nGateway dihentikan.")
            break
        except Exception as exc:
            print("gateway err:", str(exc)[:120])
            time.sleep(3)


def run(platform: str = "telegram") -> None:
    platform = (platform or "telegram").lower()
    if platform == "telegram":
        telegram()
    elif platform in ("whatsapp", "discord", "slack"):
        print(f"Gateway '{platform}' belum tersedia bawaan. Telegram sudah didukung penuh.\n"
              f"({platform} butuh integrasi tambahan — kontribusi dipersilakan.)")
    else:
        print("Platform tak dikenal. Didukung: telegram. Rencana: whatsapp, discord, slack.")
