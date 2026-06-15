# Naraya-Agent — Tools

Semua tool ada di `core/agent_tools.py` dan ter-wire ke `master_agent` (`core/rag_agent.py`, daftar `ALL_TOOLS`).
Prinsip: dependensi opsional, **gagal anggun** (mengembalikan pesan + cara setup), tidak crash saat offline.

## Daftar tool & kebutuhannya

| Tool | Fungsi | Dependensi / Env |
|------|--------|------------------|
| `web_search` | cari web (DuckDuckGo) | jaringan |
| `browser` | baca halaman (HTTP statis) | `httpx` (opsional) |
| `browser_cdp` | render situs ber-JS | `pip install playwright` + `playwright install chromium` |
| `web_automation` | klik/isi form otomatis | playwright |
| `x_search` | cari tweet | env `X_BEARER_TOKEN` |
| `eksekusi_python` | jalankan kode Python | — (subprocess bertimeout) |
| `terminal` | perintah shell | env `NARAYA_HOME` (opsional) |
| `delegate_task` | sub-agen | `agents` SDK / LLM |
| `plan_task` | rencana langkah | LLM |
| `kompres_konteks` | ringkas teks | LLM (fallback heuristik) |
| `vision_analyze` | pahami gambar | OpenAI key, `NARAYA_VISION_MODEL` (default gpt-4o-mini) |
| `generate_image` | buat gambar | OpenAI key, `NARAYA_IMAGE_MODEL` (default gpt-image-1) |
| `text_to_speech` | teks→suara | OpenAI key, `NARAYA_TTS_MODEL` (tts-1) |
| `speech_to_text` | suara→teks | OpenAI key, `NARAYA_STT_MODEL` (whisper-1) |
| `computer_*` | kontrol desktop | `pip install pyautogui pillow` |
| `send_message` | kirim pesan | `TELEGRAM_BOT_TOKEN`+`TELEGRAM_CHAT_ID` atau `NARAYA_WEBHOOK_URL` |
| `home_assistant` | rumah pintar | `HA_URL`+`HA_TOKEN` |
| `automate_schedule` | jadwalkan job | tulis ke `data/automation_jobs.json` |
| `rl_select`/`rl_feedback` | reinforcement learning (bandit) | `data/rl_bandit.db` |
| `mcp_daftar_server`/`mcp_daftar_tool`/`mcp_panggil`/`mcp_tambah_server` | MCP eksternal | `pip install mcp`, `core/mcp_servers.json` |

## Install cepat (semua opsional)

```bash
pip install httpx playwright pyautogui pillow mcp
python -m playwright install chromium
```

## Catatan keamanan
- `terminal` dan `eksekusi_python` kuat — jalankan hanya di mesin sendiri. `terminal` memblok perintah destruktif dasar (`rm -rf /`, `mkfs`, dst).
- Kunci API hanya dibaca dari environment; jangan hardcode.
