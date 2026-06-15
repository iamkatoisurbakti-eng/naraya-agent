# Session 2026-05-07 — template, audio, frame-fill, and queue hardening

Use this reference when refining the Nusantara-AI News Shorts/Instagram automation after user feedback about visible quality issues.

## User corrections captured

- Video must contain no running text/ticker/marquee/crawl/subtitle/animated text. Static Nusantara-AI News title/brand/CTA is allowed unless user asks for no text at all.
- Video title font must be clean and readable: no garbled boxes, emoji artifacts, URL/hashtag leakage, overlap, or clipping.
- Instagram 4:5 PNG must be the rendered Nusantara-AI News template/card, not just the raw generated image.
- Final audio must be clean TTS only: no backsound, music, SFX, ambience, provider audio, or extra voices.
- Template/frame should not waste empty black bars or blank space; use blurred full-bleed fill behind contained foreground media.
- Background process exit code `-15` for known old queue sessions is expected when the agent intentionally stops/restarts queues to apply config; verify the latest queue before calling it a crash.

## Implementation pattern

### No running text

- Env defaults:
  - `NEWS_NO_RUNNING_TEXT=1`
  - `NEWS_VIDEO_NO_RUNNING_TEXT=1`
- Prompt guards should prohibit: running text, ticker, crawl, subtitle, captions, lower-third motion, marquee, animated text, readable text in raw footage, posters, UI, panels, and generated letters/numbers.
- Template CSS should disable animation/transition and hide ticker/marquee elements.

### Clean title/font rendering

- Use DejaVu Sans everywhere:
  - `NEWS_TITLE_FONT_BOLD_PATH=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`
  - `NEWS_TITLE_FONT_REGULAR_PATH=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`
- Sanitize titles before overlay/manifest:
  - strip emoji, URL, hashtags such as `#Shorts`, HTML, zero-width/control chars
  - normalize whitespace, punctuation, slang/KBBI substitutions
- For ffmpeg fallback overlay, render each title line as a separate `drawtext=textfile=...` item; do not use one multiline textfile because newline glyphs can appear as boxes/garbled characters.

### Instagram 4:5 template required

- Keep `NEWS_INSTAGRAM_TEMPLATE_REQUIRED=1`.
- Save provider/raw image separately, e.g. `instagram-4x5-raw/`.
- Render final PNG by screenshotting the template `#slide` in `/root/nusantara-ai-saas/templates/nusantara_instagram_4x5.html`.
- Telegram/Facebook/report should use the templated final PNG, not raw provider image.
- Manifest should record `templateRequired`, `templated`, `templatePath`, `rawImagePath`, and final `file`.

### TTS-only audio

- Env defaults:
  - `NEWS_TTS_ONLY_AUDIO=1`
  - `NEWS_BACKSOUND_ENABLED=0`
  - `NEWS_BACKSOUND_VOLUME=0`
  - `NEWS_BACKSOUND_STYLE=none`
  - `NEWS_BACKSOUND_DUCKING=0`
- Do not pass provider `--generate-audio` when TTS-only mode is active.
- Final mux should map only the video stream and generated TTS track; discard source/provider audio.
- TTS prompt should explicitly request clean presenter voice only, no music/noise/ambience/SFX/other voices.

### Fill frame without cropping foreground

- Keep foreground media `contain` and center-safe so important subjects are not cropped.
- Fill otherwise empty/padded areas with a blurred full-bleed copy of the same media behind the foreground.
- Current preferred safe bottom values:
  - `NEWS_TEMPLATE_MEDIA_BOTTOM_SAFE=580`
  - `NEWS_TITLE_SAFE_BOTTOM=580`
- ffmpeg pattern for mismatch ratio: split video into background and foreground; background `scale=increase,crop,boxblur`, foreground `scale=decrease`, overlay foreground centered on blurred background.

### Queue restart notifications

When the CLI reports an old background process completed with exit code `-15`:

1. Treat it as expected if that process was intentionally stopped during a controlled restart.
2. Poll the latest known queue session before replying.
3. State the current active queue session/PID/status and the latest config values.
4. Do not diagnose it as a crash unless the active replacement is missing or logs show runtime failure.

## Verification probes used

- `npm run build:server`
- `bash -n scripts/run-youtube-hourly-queue.sh`
- Static scans for env/template guard strings.
- Smoke render a square source into 9:16 and sample side pixels to ensure no black padding remains.
- `ffprobe` to verify exact 1080x1920/SAR/audio stream count.
- Vision checks of rendered frames/cards for visual regressions.
