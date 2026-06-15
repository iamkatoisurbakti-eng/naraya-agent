# Session note: Telegram env loading and target fix

Date: 2026-05-08

## What happened
- `scripts/genz-news.ts --count 1` failed with:
  - `TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID belum di-set. Jalankan dengan env variable tersebut atau gunakan --dry-run.`
- `.env` already contained `TELEGRAM_BOT_TOKEN`, but the process was launched without sourcing `.env`, so the child process could not see the variables.
- The fix was to run the command as:
  - `bash -lc 'set -a; source .env; set +a; npm run gen:viral-news -- --count 1'`
- The local Telegram target list showed only:
  - `telegram:TEST (group)`
  - `telegram:Nusantara Ai (dm)`
  - `telegram:TEST / topic 225 (group)`
- For this run, `TELEGRAM_CHAT_ID` was added explicitly to `.env` so the script could send.

## Operational rules
- Do not assume `npm run` inherits `.env` automatically.
- When a news-generation or Telegram-publishing script reports missing Telegram credentials, check both:
  - the env file contents
  - whether the shell actually sourced those values before launch
- For target selection, verify the exact Telegram target mapping before sending; bare `telegram` may not be the intended public channel.
- If the intended channel/chat is known and the env key is missing, set it explicitly for the run instead of expecting the generator to infer it.

## Security note
- If a bot token is pasted into chat, tell the user to revoke/rotate it and re-enter a fresh token through the secret installer.
