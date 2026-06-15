# Session 2026-05-07: 24h YouTube queue, public articles, Indonesia audience, dynamic backsound

## Context
User requested the Nusantara-AI News automation to run as: 24 jam, 24 video, 1 jam 1 video + 1 artikel, with Telegram delivery, public YouTube Shorts, public article autoposting, Indonesian all-ages audience, real public news articles, and more engaging TTS backsound.

## Stable defaults confirmed/added
- Queue shape: `YOUTUBE_QUEUE_SLOTS=24`, `YOUTUBE_QUEUE_INTERVAL_SECONDS=3600`, `YOUTUBE_QUEUE_MONITOR_HOURS=24`, `YOUTUBE_UPLOAD_COUNT=1`.
- Article posting: `NEWS_ARTICLE_AUTOPOST=1`, `NEWS_PUBLIC_BASE_URL=https://news.nusantara-ai.online`.
- YouTube audience/locale: `YOUTUBE_MADE_FOR_KIDS=0`, `YOUTUBE_TARGET_COUNTRY=ID`, `YOUTUBE_DEFAULT_LANGUAGE=id`, `YOUTUBE_LOCATION_DESCRIPTION=Indonesia`, `YOUTUBE_CATEGORY_ID=25`.
- TTS/backsound: `NEWS_NATURAL_NARRATION=1`, `NEWS_BACKSOUND_ENABLED=1`, `NEWS_BACKSOUND_VOLUME=0.22`, `NEWS_NARRATION_VOLUME=1.16`, `NEWS_BACKSOUND_STYLE=dynamic-news-bed`, `NEWS_BACKSOUND_DUCKING=1`.
- Telegram large video guard: `NEWS_TELEGRAM_VIDEO_MAX_MB=48`; compress a Telegram preview or skip Telegram video without failing the queue.

## Code paths touched
- `scripts/news-youtube-hourly-queue.ts`: propagates env defaults and logs audience/locale fields.
- `scripts/run-youtube-hourly-queue.sh`: exports queue, article, audience, video, TTS, and backsound defaults.
- `scripts/youtube-shorts-upload.ts`: YouTube upload uses `part=snippet,status,recordingDetails`; sends `selfDeclaredMadeForKids`, language/audio language, country/location description, category 25.
- `scripts/news-video-natural-narration.ts`: generated dynamic copyright-safe news bed with sidechain ducking under the voice; TTS instructions emphasize an energetic hook and natural Indonesian Shorts delivery.
- `src/services/news-articles.ts` + `web/src/components/NewsPage.tsx`: public article pages are real short articles with sections (`Apa yang terjadi`, `Detail utama`, `Konteks dan dampak`, `Yang perlu dipantau berikutnya`) and no visible source/source button.

## Operational recipe
1. Before starting a live 24h queue, run readiness checks without printing secrets:
   - `npm run build:server`
   - `bash -n scripts/run-youtube-hourly-queue.sh`
   - confirm env statuses for YouTube OAuth, Ark/BytePlus, OpenAI, Telegram, and public base URL.
2. Stop older queue processes first to avoid double uploads:
   - match `run-youtube-hourly-queue.sh`, `news-youtube-hourly-queue.ts`, `gen:news-youtube-queue` and SIGTERM them; SIGKILL stragglers after a short wait.
3. Start the desired live queue:
   - `YOUTUBE_QUEUE_SLOTS=24 YOUTUBE_QUEUE_INTERVAL_SECONDS=3600 YOUTUBE_QUEUE_MONITOR_HOURS=24 YOUTUBE_UPLOAD_COUNT=1 NEWS_ARTICLE_AUTOPOST=1 scripts/run-youtube-hourly-queue.sh --send-telegram`
4. Verify `data/logs/youtube-hourly-queue.log` has a new `queue-start` with `slots:24`, `intervalSeconds:3600`, `monitorHours:24`, `sendTelegram:true`, `youtubeAudience:all-ages-not-made-for-kids`, `youtubeCountry:ID`, then a `slot-start` for slot 1.
5. Verify `data/logs/youtube-hourly-queue-state.json` exists.

## Pitfalls
- Background process exit code `-15` for previous queue sessions is expected after controlled restarts; explain it as SIGTERM, not a crash.
- Do not claim public article changes are live until `data/news-articles` has been synced into the running Docker volume/container and a concrete `https://news.nusantara-ai.online/news/...` URL or `/api/news/articles` returns HTTP 200.
- For CLI responses, do not emit `MEDIA:/path`; state paths plainly.
