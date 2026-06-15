# Session 2026-05-07: media generation fallback

## What happened
- Attempted to render a new flyer/video in the Nusantara-AI News pipeline session.
- Local generation was blocked because image/video provider credentials were not present in the environment.
- The standalone image tool also failed with: `FAL_KEY environment variable not set`.

## Environment state observed
- `ARK_API_KEY=missing`
- `BYTEDANCE_API_KEY=missing`
- `BYTEPLUS_API_KEY=missing`
- `OPENAI_API_KEY=missing`

## Useful fallback discovered
- Existing ready-to-use assets already live under `data/genz-news/**` and can be reused when live generation is blocked.
- The current clean Instagram/news card template is:
  - `/root/nusantara-ai-saas/templates/bot_template.html`
- That template is a black-background 4:5 editorial card with a centered pill badge and bottom title panel.

## Operational note
When a user asks for “1 flyer 1 video short sekarang” and creds are missing, prefer one of these safe outcomes:
1. deliver existing matching assets from `data/genz-news/**`, or
2. provide exact ready-to-run commands/prompt templates, clearly stating live render is blocked.

Do not claim a fresh render succeeded unless the file path has actually been produced in the current run.