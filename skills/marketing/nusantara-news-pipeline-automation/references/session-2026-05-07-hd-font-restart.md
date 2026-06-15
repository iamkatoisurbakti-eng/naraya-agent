# Session note: HD media, stable title font, and safe queue restart

Date: 2026-05-07
Repo: `/root/nusantara-ai-saas`

## User preference captured
- All generated Instagram/news images and YouTube Shorts must be HD.
- Generated/reference media must stay center-safe and uncropped in templates and prompts.
- News title typography must use one consistent font across Instagram cards, Shorts overlays, fallback SVGs, and ffmpeg drawtext overlays.
- After changing template/env/media quality settings, restart the hourly queue so active processes read the new env.

## Durable implementation pattern
- HD defaults:
  - `NEWS_IMAGE_SIZE=2K`
  - `NEWS_VIDEO_MIN_WIDTH=1080`
  - `NEWS_VIDEO_MIN_HEIGHT=1920`
  - `NEWS_VIDEO_CRF=16`
  - `NEWS_VIDEO_PRESET=slow`
  - `NEWS_VIDEO_BITRATE=10M`
- Center/seed defaults:
  - `NEWS_VISUAL_SEED=24857`
  - `NEWS_VISUAL_CENTERING_GUARD=1`
  - generated media templates should use `object-fit: contain` and `object-position: center center` plus blurred background fill.
- Title font defaults:
  - `NEWS_TITLE_FONT_FAMILY="DejaVu Sans"`
  - `NEWS_TITLE_FONT_BOLD_PATH=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`
  - `NEWS_TITLE_FONT_REGULAR_PATH=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`
  - headline selectors `#hookText` / `#titleText` should use `font-family: var(--news-title-font)`.
- Default templates:
  - Instagram 4:5: `/root/nusantara-ai-saas/templates/nusantara_instagram_4x5.html`
  - YouTube Shorts 9:16: `/root/nusantara-ai-saas/templates/nusantara_shorts_9x16.html`

## Restart verification pattern
1. Run `npm run build:server` and `bash -n` on runner scripts.
2. Check env statuses only; never print secret values.
3. Stop old `run-youtube-hourly-queue.sh` / `news-youtube-hourly-queue.ts` process tree before starting a new one.
4. Start with `scripts/run-youtube-hourly-queue.sh --send-telegram`.
5. Verify process table, log, state, and queue dir.

## Pitfall observed
HD 1080x1920 + natural narration can make Telegram `sendVideo` fail with `Request Entity Too Large`. Future fix: before Telegram video send, check file size and either compress to Telegram-safe size, send as document only if allowed, or skip Telegram video without failing the entire YouTube queue slot.