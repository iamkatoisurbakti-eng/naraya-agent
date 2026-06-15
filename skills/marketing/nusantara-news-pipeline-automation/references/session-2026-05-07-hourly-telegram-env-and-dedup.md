# Session note: hourly Telegram pack, env propagation, and dedup

## What happened
- Hourly news automation was used to generate 1 unique flyer PNG per run and send it to Telegram.
- The generator could render the PNG successfully, but the Telegram send path failed in one background execution because `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` were not available inside the spawned process.
- A manual Telegram send using the resulting PNG succeeded afterward.

## Working lesson
- For scheduled/background runs, ensure Telegram env vars are present in the *child process* itself, not only in the parent shell.
- If the generator requires a Telegram destination and the env is missing, either inject a temporary chat id (`-1003922584410` in this session) or run a dry-run / manual send path.
- The bare `telegram` target may resolve to the home channel or another mapped destination; verify the exact destination mapping before assuming it is the public channel.

## Deduplication note
- Hourly slots should keep a strict uniqueness gate so the job skips near-duplicates rather than filling the slot with a reworded repeat.
- If no unique item clears the score threshold, skip the slot cleanly instead of forcing output.
