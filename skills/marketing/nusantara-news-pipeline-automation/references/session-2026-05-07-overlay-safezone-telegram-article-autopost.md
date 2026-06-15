# Session 2026-05-07: Overlay safe-zone, Telegram HD guard, and article autopost

Context: User iteratively tightened the Nusantara-AI News automation after the 12-slot YouTube/Telegram queue was running live. Key corrections were production quality preferences: titles must use a consistent font, images/videos must not collide with title overlays, HD media must still fit Telegram delivery, and each generated story must autopost to the public Nusantara-AI News platform.

## Durable implementation details

- Title consistency:
  - Use `NEWS_TITLE_FONT_FAMILY="DejaVu Sans"`.
  - Use `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf` and `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` for ffmpeg drawtext/fallback overlays.
  - HTML templates should define `--news-title-font` and assign it to `#hookText` / `#titleText`.

- Overlay collision prevention:
  - Keep `NEWS_VISUAL_OVERLAY_SAFE_ZONE=1` and `NEWS_TITLE_SAFE_BOTTOM=430`.
  - Shorts template should reserve the lower title/CTA area instead of letting media fill the entire canvas behind text.
  - ffmpeg title overlay should scale/pad the source video into the upper visual area and draw a dark title-safe bottom panel.
  - Prompts must say important people/objects/actions stay in upper/middle safe area while lower ~30–35% remains simple/dark/low-detail.

- Telegram HD video size guard:
  - HD 1080x1920 + narration can exceed Telegram Bot upload limits (`Request Entity Too Large`).
  - `NEWS_TELEGRAM_VIDEO_MAX_MB=48` is the default threshold.
  - Before `sendVideo`, check size; if too large, create a Telegram-only preview/compressed MP4. If that still exceeds threshold, skip Telegram video safely without failing the queue slot. Do not reduce YouTube HD master quality.

- Article autopost to Nusantara-AI News:
  - `scripts/genz-news.ts` already saves generated articles to `data/news-articles` via `saveGeneratedNewsArticles`.
  - Pipeline should explicitly gate/report this as `post-news-platform` when `NEWS_ARTICLE_AUTOPOST=1`.
  - Default public base: `NEWS_PUBLIC_BASE_URL=https://news.nusantara-ai.online`.
  - Validate both local data and public route:
    - `data/news-articles/index.json` exists and has articles.
    - `curl -kfsSI https://news.nusantara-ai.online/news` returns success.
    - A concrete article URL from the index returns HTTP 200.
  - Include the public article URL in Telegram/YouTube/Facebook captions when available.

## Restart/verification pattern

After changing env passthrough or live pipeline behavior:
1. Run `npm run build:server`.
2. Run `bash -n scripts/run-youtube-hourly-queue.sh` and relevant wrapper syntax checks.
3. Stop only queue-related processes: `run-youtube-hourly-queue.sh`, `news-youtube-hourly-queue.ts`, `gen:news-youtube-queue`.
4. Restart with `scripts/run-youtube-hourly-queue.sh --send-telegram`.
5. Poll the process/session and inspect `data/logs/youtube-hourly-queue.log` for `queue-start` + `slot-start`.

Exit code `-15` on older background sessions is expected if it was an intentional SIGTERM during controlled restart; explain this directly so the user does not treat it as a crash.
