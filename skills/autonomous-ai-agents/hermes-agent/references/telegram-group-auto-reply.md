# Telegram group auto-reply notes

Use these settings for Hermes in Telegram groups:

- `telegram.require_mention: false` = reply to all group messages without an @mention.
- `telegram.require_mention: true` + `telegram.free_response_chats: ["-100..."]` = auto-reply only in selected group chat IDs.
- `telegram.reply_to_mode: first` is the default and keeps multi-chunk replies threaded only on the first chunk.

Operational notes:

- After editing `~/.hermes/config.yaml`, restart the gateway: `hermes gateway restart`.
- If `hermes gateway start` says the service is not installed, run `hermes gateway install` first, then start again.
- `hermes gateway status` confirms the active service state.
- Telegram group IDs are negative strings/numbers, usually beginning with `-100`.

Relevant config keys are bridged from `telegram:` in `config.yaml` into env vars at startup, so YAML changes require a gateway restart to take effect.