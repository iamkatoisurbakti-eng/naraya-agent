# Session 2026-05-07: Natural presenter narration + safe secret installer

## What changed

Nusantara-AI News pipeline gained a post-processing step for more natural news-anchor narration:

- New script: `/root/nusantara-ai-saas/scripts/news-video-natural-narration.ts`
- New npm command: `npm run gen:news-video:natural-narration`
- Integrated into `/root/nusantara-ai-saas/scripts/news-pipeline.ts` after title overlay.
- `finalVideoManifestPath` now points to the narrated manifest when narration succeeds, so Telegram/YouTube use the narrated MP4.
- If `OPENAI_API_KEY` is missing or dry-run is active, narration writes a manifest and safely falls back to the titled video.

## Runtime/env defaults

- `NEWS_NATURAL_NARRATION=1`
- `NEWS_TTS_MODEL=gpt-4o-mini-tts`
- `NEWS_TTS_VOICE=verse`
- Requires `OPENAI_API_KEY` for live TTS.
- Uses OpenAI `/audio/speech` with instructions for natural Indonesian news-anchor delivery.
- Uses `ffmpeg` to mux TTS audio into MP4 and `ffprobe` to match video duration.

## Safe secret handling added

User pasted ARK/OpenAI keys into chat. Do not reuse exposed keys from transcript. Recommend rotate/regenerate, then store new keys outside chat.

Added:

- `/root/nusantara-ai-saas/scripts/set-news-automation-secrets.sh`
  - prompts with hidden input for `ARK_API_KEY` and `OPENAI_API_KEY`
  - upserts into `.env` with `chmod 600`
  - mirrors ARK into `BYTEDANCE_API_KEY` and `BYTEPLUS_API_KEY`
  - sets news automation defaults
  - prints only set/missing status, never values
- `/root/nusantara-ai-saas/.gitignore`
  - ignores `.env` and `.env.*`
- `/root/nusantara-ai-saas/.env.example`
  - placeholder keys and news automation defaults

## Verification commands used

```bash
bash -n scripts/set-news-automation-secrets.sh
npm run build:server
npm run gen:news-video:natural-narration -- --dry-run \
  --video-manifest /tmp/nusantara-narration-test/video-manifest.json \
  --news-manifest /tmp/nusantara-narration-test/news-manifest.json \
  --output-manifest /tmp/nusantara-narration-test/out.json
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 /tmp/nusantara-narration-test/input.mp4
```

## Pitfalls

- Never write secrets from chat transcript into `.env`; ask user to rotate and run the prompt-based installer locally.
- Do not echo real key values in terminal output or final responses; use `[REDACTED]` or set/missing.
- `NEWS_NATURAL_NARRATION=1` should not break pipeline when OpenAI is missing; keep fallback behavior.
- Telegram should still send only complete image+video pairs after final video manifest resolution.
