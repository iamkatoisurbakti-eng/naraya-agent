# Session 2026-05-07: `.env.example` secret leak cleanup and validation

## Trigger

During Nusantara AI SaaS automation setup, `.env.example` was inspected and found to contain real-looking secrets/tokens instead of placeholders:

- ARK/BytePlus key values
- OpenAI API key
- Telegram bot token
- YouTube OAuth client secret
- Cloudflare API token
- Hostinger API token

The file was immediately rewritten as a safe template with blank secret fields and non-secret defaults only.

## Rule for future sessions

`.env.example` is public/template material. It must never contain real secrets, even if the repo is not a git worktree. Only these are acceptable:

- blank placeholders: `OPENAI_API_KEY=`
- safe defaults: `NEWS_MIN_SCORE=90`, `NEWS_INSTAGRAM_ASPECT=4:5`
- non-secret identifiers only when needed, but prefer blanks for OAuth client fields too

Actual credentials belong only in `.env`, deployment env, or a credential manager, with `.env` mode `600` and gitignored.

## Validation pattern

Use a safe scanner before/after touching env files. Do not print matched secret values.

```bash
cd /root/nusantara-ai-saas
python3 - <<'PY'
from pathlib import Path
import re, json
p=Path('.env.example')
s=p.read_text(errors='ignore') if p.exists() else ''
patterns={
 'ark_like': r'ark-[A-Za-z0-9-]{20,}',
 'openai_like': r'sk-[A-Za-z0-9_-]{20,}',
 'telegram_bot_like': r'\b\d{8,12}:[A-Za-z0-9_-]{25,}\b',
 'google_oauth_secret_like': r'GOCSPX-[A-Za-z0-9_-]+',
 'cloudflare_token_like': r'\bcfat_[A-Za-z0-9_-]+\b',
}
print(json.dumps({k: bool(re.search(v,s)) for k,v in patterns.items()}, indent=2))
PY
```

All values should be `false` for `.env.example`.

## Safe `.env.example` shape

Keep this class of content:

```dotenv
ARK_API_KEY=
BYTEDANCE_API_KEY=
BYTEPLUS_API_KEY=
OPENAI_API_KEY=
TELEGRAM_BOT_TOKEN=
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN=
CLOUDFLARE_API_TOKEN=
HOSTINGER_API_TOKEN=
NEWS_MIN_SCORE=90
NEWS_MIN_SINGLE_SCORE=90
NEWS_INSTAGRAM_ASPECT=4:5
TELEGRAM_PUBLIC_CHANNEL_NAME=@nusantaranewsindonesia
```

## YouTube OAuth pitfall found

`YOUTUBE_REFRESH_TOKEN=https://oauth2.googleapis.com/token` is invalid; that is the token endpoint URL, not a refresh token. A real refresh token is obtained only after the user authorizes the OAuth URL and the returned code is exchanged.

## Response posture

If leaked secrets are found in `.env.example` or chat:

1. Sanitize the file immediately.
2. Report only secret classes/status, never raw values.
3. Tell the user to rotate/regenerate exposed credentials.
4. Store new credentials only via prompt-based installer or direct env injection.
