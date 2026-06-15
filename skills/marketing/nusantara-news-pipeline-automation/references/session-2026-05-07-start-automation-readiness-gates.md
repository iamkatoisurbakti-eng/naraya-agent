# Session note: start automation readiness gates

When user says `startautomation` / `start queue youtube sekarang`, do not blindly start the 12-slot queue. First perform an env readiness gate and process check.

## Required checks

1. Check running processes to avoid duplicate queues:
   - `process list` if available
   - `pgrep -af 'news-youtube-hourly-queue|gen:news-youtube-queue|run-youtube-hourly-queue' || true`
2. Load `.env` with dotenv and print only set/missing statuses.
3. Require all live queue prerequisites before starting:
   - YouTube OAuth: `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`
   - Image/video provider: any of `ARK_API_KEY`, `BYTEDANCE_API_KEY`, `BYTEPLUS_API_KEY`
   - Natural narration: `OPENAI_API_KEY` when `NEWS_NATURAL_NARRATION=1`
4. Ensure non-secret defaults are present in `.env`:
   - `NEWS_MIN_SCORE=90`
   - `NEWS_MIN_SINGLE_SCORE=90`
   - `NEWS_INSTAGRAM_ASPECT=4:5`
   - `YOUTUBE_QUEUE_SLOTS=12`
   - `YOUTUBE_QUEUE_INTERVAL_SECONDS=3600`
   - `YOUTUBE_QUEUE_MONITOR_HOURS=24`
   - `YOUTUBE_PRIVACY_STATUS=public`

## Pitfall

If YouTube OAuth is valid but ARK/BytePlus or OpenAI are missing, do not start the live queue. It will fail during image/video generation or natural narration. Tell the user exactly which credentials are missing and provide the prompt-based installer command.

## Safe response pattern

- If ready: start `scripts/run-youtube-hourly-queue.sh` in background, then verify log/state.
- If not ready: do not start; write/set non-secret defaults only and report missing credentials.