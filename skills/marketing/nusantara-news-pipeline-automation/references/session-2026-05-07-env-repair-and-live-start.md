# 2026-05-07 env repair + live YouTube queue start

Context: user asked to re-check `.env` and start automation only if everything was complete.

Reusable lessons:

- Validate `.env` structurally before starting: existence, `0600` mode, no malformed non-comment lines, required keys present, no duplicate queue process.
- A malformed Telegram line appeared as `TELEGRAMBOT:<token>` (no `=`). Treat this as invalid `.env` syntax but recoverable: if it matches a Telegram bot token pattern, convert it to `TELEGRAM_BOT_TOKEN=<token>` without printing the token, then re-validate.
- Ensure non-secret runtime defaults are present before starting queue:
  - `NEWS_MIN_SCORE=90`
  - `NEWS_MIN_SINGLE_SCORE=90`
  - `NEWS_INSTAGRAM_ASPECT=4:5`
  - `YOUTUBE_QUEUE_SLOTS=12`
  - `YOUTUBE_QUEUE_INTERVAL_SECONDS=3600`
  - `YOUTUBE_QUEUE_MONITOR_HOURS=24`
  - `NEWS_NATURAL_NARRATION=1`
  - `NEWS_TTS_MODEL=gpt-4o-mini-tts`
  - `NEWS_TTS_VOICE=verse`
  - `YOUTUBE_PRIVACY_STATUS=public`
  - `TELEGRAM_PUBLIC_CHANNEL_NAME=@nusantaranewsindonesia`
- Before live start, run live-safe credential probes without printing secrets:
  - YouTube OAuth refresh token exchange against `https://oauth2.googleapis.com/token` should return HTTP 200 and access token status `set`.
  - Telegram `getMe` should return `ok: true`.
  - OpenAI `/v1/models` should return HTTP 200.
  - TypeScript server build should pass.
- Start queue with `scripts/run-youtube-hourly-queue.sh` only after readiness gates pass.
- Verify start by checking:
  - background session/process is running
  - `data/logs/youtube-hourly-queue.log` exists and grows
  - `data/logs/youtube-hourly-queue-state.json` exists
  - process tree includes `news-youtube-hourly-queue.ts --slots 12 --interval-seconds 3600 --monitor-hours 24`

Do not print raw values from `.env`, OAuth redirect URLs, access tokens, refresh tokens, or Telegram bot tokens in final responses. Report only `set`/`missing`/`ok` statuses.
