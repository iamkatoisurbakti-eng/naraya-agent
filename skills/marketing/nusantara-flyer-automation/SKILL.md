---
name: nusantara-flyer-automation
description: Generate Nusantara-AI News 4:5 flyer PNGs from live news, using the repo's Instagram flyer template, score gate, and manifest/report outputs.
---

# Nusantara Flyer Automation

Use this skill when the user asks to create, update, or troubleshoot a single news flyer for Nusantara-AI News.

## What this produces
- 1 Instagram-style news flyer in 4:5 PNG format
- a matching `manifest.md` / `manifest.json` in the run directory
- optional Telegram delivery when credentials exist

## Source of truth
- Generator: `/root/nusantara-ai-saas/scripts/genz-news.ts`
- Template: `/root/nusantara-ai-saas/templates/nusantara_instagram_4x5.html`
- Output root: `/root/nusantara-ai-saas/data/genz-news/<timestamp>/`
- Article index: `/root/nusantara-ai-saas/data/news-articles/index.json`
- Prompt enhancer reference: `references/openai-prompt-enhancer.md` (GPT-4o can rewrite a raw flyer prompt before image generation; keep this as a separate rewrite stage, not a replacement for the image provider)
- Session note for GPT-4o + Seedream limits: `references/session-2026-05-08-gpt4o-seedream-seedance-limits.md`

## Default workflow
1. Generate one flyer:
   - `npm run gen:viral-news -- --count 1 --dry-run`
2. Inspect the newest `data/genz-news/<timestamp>/` directory.
3. Verify the PNG exists and is 1080x1350.
4. Read `manifest.md` to confirm the title, caption, hashtags, and article URL.
5. If you want the flyer prompt to be polished first, set `NEWS_FLYER_PROMPT_PROVIDER=openai` and `NEWS_FLYER_PROMPT_MODEL=gpt-4o`, then run the image generator through `scripts/prompt-to-images.ts` or the news pipeline.
6. If Telegram sending is desired, run without `--dry-run` only when `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set.

## Visual rules for the flyer
- Keep the image full-frame and editorial, not like a plain poster.
- Use the `nusantara_instagram_4x5.html` template as the final presentation layer.
- Prefer a stronger fill/cover look for the hero image so the frame feels full.
- Keep the title panel readable, clean, and not crowded.
- Preserve Nusantara-AI News branding.
- Do not show source labels in the public-facing flyer.
- Do not show slide counters or item numbers like `01`; every flyer should appear as a standalone piece.

## What to verify
- PNG file exists in the run directory
- image dimensions are `1080 x 1350`
- `manifest.md` contains one item with title, *full caption*, and hashtags
- captions must not be truncated/ellipsis-style; use a complete caption block
- every flyer must carry exactly 4 hashtags unless the user explicitly asks otherwise
- if Telegram sending was attempted, confirm the send result before claiming success

## Common pitfall
- `genz-news.ts` can render the flyer and still exit non-zero if Telegram env vars are missing, because it expects `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` for the send step.
- If the user only wants the flyer asset, prefer `--dry-run` so the run completes without the Telegram requirement.
- OpenAI prompt enhancement can succeed even when the downstream image provider fails; do not confuse a good rewritten prompt with a successful render.
- OpenAI image rendering may be blocked by org verification, and Ark rendering may fail on account balance issues; verify provider readiness before promising output. See `references/session-2026-05-08-openai-flyer-prompt-enhancer-and-provider-gates.md`.

## Output style
- Keep flyers concise and news-like.
- Follow the user's Nusantara-AI News branding conventions.
- Prefer direct verification over assumptions.
