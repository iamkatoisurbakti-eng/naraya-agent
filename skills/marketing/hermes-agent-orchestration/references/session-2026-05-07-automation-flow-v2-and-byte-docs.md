# Session 2026-05-07 — Automation Flow V2 + BytePlus/ARK Docs Integration

Context: user asked to add `/root/.hermes/Byte1` through `/root/.hermes/Byte14` to Nusantara-AI automation, then asked to define a new automation flow.

## Durable repo artifacts

- Flow config: `/root/nusantara-ai-saas/config/automation-flow-v2.json`
- Flow docs: `/root/nusantara-ai-saas/docs/automation-flow-v2.md`
- Byte docs index: `/root/nusantara-ai-saas/config/byteplus-ark-automation.json`
- Byte docs indexer/validator: `/root/nusantara-ai-saas/scripts/byteplus-docs-index.mjs`
- BytePlus reference in pipeline skill: `nusantara-news-pipeline-automation/references/byteplus-ark-byte1-byte14-automation.md`

## Flow V2 stages

```text
collect_sources
  -> ideation_scoring
  -> filter_idea
  -> script_writing
  -> filter_script
  -> visual_audio_packet
  -> render_media
  -> filter_render_metadata
  -> quality_check
  -> schedule_publish
  -> distribution
```

## Non-negotiable gates

- Score gates: idea/script/QC >=90.
- Skip slot instead of forcing weak/duplicate content.
- Filter Agent PASS required before script, before visual/audio, and before publish/QC handoff.
- QC must be `PUBLISH` before Scheduler may upload/schedule.
- Video max 30 seconds, target 20-30 seconds, 2 scenes × 15 seconds.
- Video 9:16 1080x1920, prompt-only text-to-video, no reference image by default.
- No OpenAI TTS by default; generated-video/SEEDANCE ambience/action audio only.
- No watermark, no running text/ticker/subtitles in generated footage.
- Instagram/news image final output must be the 4:5 template card, not raw provider image.
- Telegram only after image + final video exist.
- YouTube upload only via OAuth refresh token, not API key.
- Credentials and signed URLs must never be printed.

## Byte docs mapping

- Byte1/Byte2: ARK `/chat/completions`; use for analyzer/visual-understanding references only, not as factual news source.
- Byte3: Hitem3D; disabled/reference-only for Shorts/news.
- Byte4: primary Seedance video-generation API reference.
- Byte5: primary Seedream image-generation API reference.
- Byte6: optional embedding/retrieval/semantic dedupe reference.
- Byte7/8/12/14: Seedance image-to-video task examples.
- Byte13: Seedance text-to-video example; important for Nusantara-AI prompt-only video mode.
- Byte9/11: Seedream text-to-image examples.
- Byte10: SeedEdit image-to-image example.

## Validation performed

- `node scripts/byteplus-docs-index.mjs` returned 14 docs present, 12 active, all sanitized, no secret printed.
- `npm run build:server` passed after endpoint/config integration.
- `prompt-to-images.ts --dry-run` used `/images/generations`, Seedream model, 2K, watermark false.
- `images-to-video.ts --dry-run` used `/contents/generations/tasks`, 30s, 2 scenes, 9:16, generated audio true, watermark false.
- `config/automation-flow-v2.json` parsed successfully with 11 stages.

## Provider blocker handling

If BytePlus/ARK returns HTTP 403 `AccountOverdueError`, treat it as a provider billing blocker and set slot decision `RETRY_LATER` or `SKIP_SLOT`; do not debug YouTube/Telegram/code path as root cause unless other evidence appears.
