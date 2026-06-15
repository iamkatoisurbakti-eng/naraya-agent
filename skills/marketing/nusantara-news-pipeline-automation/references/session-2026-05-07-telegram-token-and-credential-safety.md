# Session 2026-05-07 — Telegram token + credential safety for news automation

Context:
- User asked to store ARK, OpenAI, Gmail password, and Telegram bot token for Nusantara-AI News automation.
- Several credentials were pasted directly into chat. Treat pasted secrets as compromised; do not copy them into files, scripts, logs, final answers, memory, or skills.

Implemented/confirmed patterns:
- Use prompt-based secret installers that read with `read -s` and write to `.env` with `chmod 600`.
- Print only `set` / `missing` status for secrets.
- Keep `.env` gitignored and provide `.env.example` placeholders only.
- Extend `/root/nusantara-ai-saas/scripts/set-news-automation-secrets.sh` to support:
  - `ARK_API_KEY`
  - `BYTEDANCE_API_KEY`
  - `BYTEPLUS_API_KEY`
  - `OPENAI_API_KEY`
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_PUBLIC_CHANNEL_NAME=@nusantaranewsindonesia`
  - natural narration env defaults.
- Verification command used:
  - `bash -n scripts/set-news-automation-secrets.sh`
  - scan installer content to ensure raw token substrings were not persisted.

Important workflow rule:
- If the user pastes a Telegram bot token/API key/password into chat and asks to save it, refuse to persist the pasted value. Tell them to rotate/regenerate the secret and enter the fresh value through the prompt-based installer.

Gmail/login rule:
- Do not store Gmail account passwords for Hostinger/Cloudflare/BytePlus automation.
- Use provider-specific API tokens/OAuth instead:
  - Cloudflare: scoped `CLOUDFLARE_API_TOKEN`
  - Hostinger: provider API token if available
  - BytePlus/ARK: `BYTEPLUS_API_KEY` / `ARK_API_KEY`
  - Google/Gmail: OAuth/App Password, not the main account password.

Telegram production reminders:
- `TELEGRAM_BOT_TOKEN` must be present in env.
- Bot must be admin in `@nusantaranewsindonesia` before sends can succeed.
- Public target stays env-driven and normalized by the pipeline.
