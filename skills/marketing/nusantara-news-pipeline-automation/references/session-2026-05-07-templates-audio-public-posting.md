# Session 2026-05-07 — templates, audio, CTA, and queue restart notes

Context: Nusantara-AI News automation was updated for production queueing with public article links, Instagram/Shorts templates, natural Indonesian narration, backsound, CTA subscribe, and Telegram-enabled queue restart.

## Durable project decisions

- Public article URL base is `NEWS_PUBLIC_BASE_URL=https://news.nusantara-ai.online`; captions/reports should convert relative `/news/...` paths to absolute public URLs.
- Instagram/news image template is `/root/nusantara-ai-saas/templates/bot_template.html` via `NEWS_IMAGE_CARD_TEMPLATE_PATH`.
- YouTube Shorts video overlay template is `/root/nusantara-ai-saas/templates/genz.html` via `NEWS_VIDEO_OVERLAY_TEMPLATE_PATH`.
- Video overlay template should be 1080x1920 / 9:16 with Nusantara-AI News branding and visual subscribe CTA.
- Instagram template should be 1080x1350 / 4:5 and must expose renderer-compatible DOM IDs.
- Natural narration defaults:
  - `NEWS_TTS_MODEL=gpt-4o-mini-tts`
  - `NEWS_TTS_VOICE=verse`
  - `NEWS_TTS_VOICE_LOCK=1`
  - `NEWS_TTS_CHARACTER="Presenter berita Indonesia laki-laki dewasa muda, natural, ramah, tegas, artikulasi jelas, beraksen Indonesia netral, cocok untuk YouTube Shorts berita Gen-Z."`
- Backsound defaults:
  - `NEWS_BACKSOUND_ENABLED=1`
  - `NEWS_BACKSOUND_VOLUME=0.16`
  - `NEWS_NARRATION_VOLUME=1.12`
  - If `NEWS_BACKSOUND_PATH` is empty, generate a subtle copyright-safe ffmpeg news bed instead of random music.
- End narration CTA default:
  - `NEWS_END_CTA_SUBSCRIBE="Sebelum lanjut scroll, jangan lupa subscribe channel Nusantara-AI News, aktifkan loncengnya, dan bagikan video ini kalau menurut kamu penting."`

## Template compatibility pitfall

`scripts/genz-news.ts` screenshots `#slide` and fills these IDs when rendering Instagram/news cards:

- `#slide` — screenshot target
- `#hookText` — title
- `#descText` — summary
- `#catPill` — category/brand label
- `#slideCounter` — counter text
- `#imgZone` — main image container
- optional `#dots` — pagination dots

If `bot_template.html` only has `#news-card`/`#news-title`, Playwright fails with:

```text
locator.screenshot: Timeout 30000ms exceeded
- waiting for locator('#slide')
```

Fix by rewriting/patching the template to expose the expected IDs, then validate with:

```bash
cd /root/nusantara-ai-saas
NEWS_MIN_SCORE=90 NEWS_MIN_SINGLE_SCORE=90 NEWS_INSTAGRAM_ASPECT=4:5 \
  npm run gen:viral-news -- --count 1 --dry-run --template /root/nusantara-ai-saas/templates/bot_template.html
```

## Queue restart and Telegram flag pitfall

`scripts/run-youtube-hourly-queue.sh` must forward extra args (`"$@"`) to `npm run gen:news-youtube-queue`; otherwise `scripts/run-youtube-hourly-queue.sh --send-telegram` appears accepted at the shell level but queue starts with `sendTelegram:false`.

Expected tail of the runner command:

```bash
npm run gen:news-youtube-queue -- \
  --slots "$YOUTUBE_QUEUE_SLOTS" \
  --interval-seconds "$YOUTUBE_QUEUE_INTERVAL_SECONDS" \
  --monitor-hours "$YOUTUBE_QUEUE_MONITOR_HOURS" \
  "$@"
```

When restarting:

1. Stop old queue PIDs (`run-youtube-hourly-queue.sh`, `gen:news-youtube-queue`, `news-youtube-hourly-queue.ts`). Background completion with exit code `-15` is normal SIGTERM for the old stopped process.
2. Run readiness gates without printing secrets: `.env` syntax/mode, `npm run build:server`, YouTube OAuth token refresh HTTP 200 with scope `youtube.upload`, OpenAI `/v1/models` HTTP 200, Telegram `getMe` ok.
3. Start new queue:

```bash
cd /root/nusantara-ai-saas
scripts/run-youtube-hourly-queue.sh --send-telegram
```

4. Verify process/log:

```bash
ps -eo pid,args | grep -E 'run-youtube-hourly-queue|gen:news-youtube-queue|news-youtube-hourly-queue' | grep -v grep
python3 - <<'PY'
from pathlib import Path
import json
log=Path('/root/nusantara-ai-saas/data/logs/youtube-hourly-queue.log')
for l in log.read_text(errors='replace').splitlines()[::-1]:
    if 'queue-start' in l or 'slot-start' in l:
        print(l[:500]); break
PY
```

Look for `sendTelegram:true`, `slots:12`, `intervalSeconds:3600`, `monitorHours:24`.

## .env quoting pitfall

Values containing spaces must be quoted for shell sourcing, even though `dotenv` can parse them unquoted. Quote at least:

- `NEWS_TTS_CHARACTER="..."`
- `NEWS_END_CTA_SUBSCRIBE="..."`

Otherwise `set -a; . ./.env` can fail with errors like `berita: command not found`.

## YouTube upload manifest pitfall

Older `youtube-shorts-upload.ts` only accepted `titleVideoPath || videoPath || filePath`. If natural narration produces `rawVideoPath`, `sourcePath`, or `titleVideoPath` variants, keep upload/title scripts compatible with all manifest fields used by upstream generation.

## Validation checklist after these changes

- `npm run build:server`
- `bash -n scripts/run-youtube-hourly-queue.sh`
- `bash -n scripts/youtube-scheduled-upload.sh`
- template dry-run succeeds with `bot_template.html`
- ffprobe on a rendered Short returns 1080x1920 and audio present
- queue log has fresh `queue-start` with `sendTelegram:true` when user asked Telegram enabled
- `.env.example` scan has no real secrets
