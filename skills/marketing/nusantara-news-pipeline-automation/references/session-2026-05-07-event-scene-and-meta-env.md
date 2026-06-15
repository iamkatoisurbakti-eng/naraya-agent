# Session 2026-05-07: Event-scene visual guard + Meta env cleanup

## User corrections/preferences

- Generated news visuals should depict the event/scene/behavior described by the story.
- Do not generate text-heavy posters, typography, fake headlines, lower-thirds, UI, watermarks, or source labels inside AI-generated images/video footage.
- Do not generate reporters/news anchors/presenters, TV studios, newsroom desks, microphone interviews, or people speaking directly to camera. Show the behavior/action/context of the story instead.
- User authorizes direct production-focused code/platform changes in `/root/nusantara-ai-saas` when evaluation/scoring is 90+; still verify and avoid exposing secrets.

## Implemented pattern

- `scripts/news-pipeline.ts`
  - `buildInstagramPrompt(...)` now asks for a concrete event/behavior scene and explicitly forbids text/posters/reporter/news-anchor imagery.
  - `buildVideoPrompt(...)` now asks for raw 9:16 footage as a sequence of actions/behavior/context, not presenter/newsroom shots.
  - Image generation args use `--watermark=false`.
- `scripts/genz-news.ts`
  - `buildSeedreamPrompt(...)` tone changed from cover/newsroom hero image to real-world incident/documentary/event scene.
  - Prompt forbids reporters, news anchors, presenters, newsroom/studio, mic interviews, readable signs, text/logo/watermark/UI.
- `scripts/prompt-to-images.ts`
  - Added `NEWS_IMAGE_EVENT_SCENE_ONLY=1` guard that appends a strict event/action scene negative prompt to every image request.
- Queue/scheduled/Docker/env defaults carry `NEWS_IMAGE_EVENT_SCENE_ONLY=1`.

## Validation used

```bash
npm run build:server
bash -n scripts/run-youtube-hourly-queue.sh
bash -n scripts/youtube-scheduled-upload.sh
NEWS_IMAGE_EVENT_SCENE_ONLY=1 npx tsx scripts/prompt-to-images.ts --dry-run --provider ark --prompt 'Judul: demo; buat cover berita' --output /tmp/event-scene-test.png --watermark=false
```

Check parsed payload includes:
- `STRICT VISUAL GUARD`
- `concrete event/action scene`
- `reporter`, `news anchor`, `presenter` in negative guard
- `Do not generate text` / `typography`
- `watermark === false`

## Meta/Facebook env cleanup

User asked to check `.env` Facebook link Meta. Found malformed prose-like key, redacted here:

```env
facebook business meta : https://business.facebook.com/...
```

Normalize to valid env:

```env
META_BUSINESS_LINK="https://business.facebook.com/..."
```

Then validate with dotenv only returning booleans:
- `META_BUSINESS_LINK` set
- starts with `https://business.facebook.com/`
- old malformed key absent
- `.env` remains mode `600`

Note: a Business Manager share link is not enough for auto-posting. Real Facebook/Meta posting needs official Graph API credentials such as Page ID and Page Access Token; do not claim Meta posting is live from the link alone.
