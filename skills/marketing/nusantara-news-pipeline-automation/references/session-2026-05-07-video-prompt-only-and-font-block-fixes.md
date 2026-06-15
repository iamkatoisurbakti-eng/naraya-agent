# Session 2026-05-07: video prompt-only mode + font/block fixes

## User corrections captured

- Video generation must not use the Instagram 4:5 image as a reference unless explicitly requested.
- The video stage should build a cinematic realistic action prompt directly from the news item.
- Instagram/news PNG must not look like an old poster block; large font must not cover the hero/image block.

## Implemented project behavior

- `NEWS_VIDEO_USE_REFERENCE_IMAGE=0` is the default no-reference video mode.
- `scripts/news-pipeline.ts` only passes `--image-url` to `scripts/images-to-video.ts` when `NEWS_VIDEO_USE_REFERENCE_IMAGE=1` and a reference URL exists.
- In no-reference mode, video prompt text explicitly says to create the video directly from the news prompt and not from Instagram 4:5 image reference.
- The pipeline may still render Instagram 4:5 cards for Telegram/Facebook/news assets, but the video stage is decoupled from that image.
- If Instagram image generation fails while no-reference video mode is active, do not automatically block the video stage solely because there is no Instagram reference image. Only block for missing reference when `NEWS_VIDEO_USE_REFERENCE_IMAGE=1`.

## Prompt rules for video stage

Prompt should include:

- cinematic realistic Indonesian news action scene
- generated directly from news facts, not reference-image guided
- event/behavior/action sequence: people, location, atmosphere, props, public/police/official response when relevant
- generic realistic/fictitious people and locations when needed for copyright safety
- no reporter, no anchor, no newsroom/studio
- no readable text, ticker, subtitles, lower-third, marquee, crawl, posters, or UI
- no watermark, logos, brand/IP imitation, celebrity impersonation, TV/movie/social clip mimicry
- generated ambience/action audio may exist but no dialog/voice-over/music imitation when final mix uses TTS + generated-video audio

## Font/template fixes

- Use `/root/nusantara-ai-saas/templates/nusantara_instagram_4x5.html` as the primary Instagram card template.
- Keep headline adaptive and bounded in `scripts/genz-news.ts` before screenshot rendering.
- Avoid defining helper functions with default parameters inside `page.evaluate` if Playwright/tsx transpilation injects `__name`; inline the fit loops or avoid default params to prevent `page.evaluate: ReferenceError: __name is not defined`.
- Instagram template should use DejaVu/Arial fallback, smaller headline defaults, limited text height, hidden overflow, and bigger hero area so headline never covers the image block.

## Validation commands used

```bash
npm run build:server
bash -n scripts/run-youtube-hourly-queue.sh
NEWS_VIDEO_USE_REFERENCE_IMAGE=0 NEWS_GENERATED_VIDEO_AUDIO_ENABLED=1 NEWS_VIDEO_CINEMATIC_REALISM=1 \
  npx tsx scripts/images-to-video.ts --dry-run \
  --prompt "Berita Indonesia: aksi penyelamatan warga di pelabuhan, cinematic realistic action, no text" \
  --output /tmp/no-ref-video.mp4 --ratio 9:16 --duration 60 --generate-audio --watermark=false --seed 24857
```

Expected dry-run property: scene payloads contain no `image_url` content.

## Operational notes

- Restart queue after changing env/path behavior so the new background command shows `NEWS_VIDEO_USE_REFERENCE_IMAGE=0`.
- If old background processes exit with code `-15`, treat as expected controlled SIGTERM from restart, not a crash.
- ARK/BytePlus `AccountOverdueError` remains a provider/billing blocker and is not fixed by no-reference mode.
