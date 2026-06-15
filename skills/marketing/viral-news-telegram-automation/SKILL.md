---
name: viral-news-telegram-automation
description: Generate 10 safe viral news flyers with Seedream/ARK, render via bot_template.html, and send each PNG to Telegram with caption + hashtags.
---

# Viral News Telegram Automation

Use this skill when the user wants a repeatable flow to:
- pick 10 latest viral news items
- exclude religion, politics, and sexual content
- generate images with Byte/ARK Seedream
- render one PNG per item with a consistent template
- send the final pack to Telegram with caption + hashtags
- or produce a single ready-to-post 4:5 news feed card with the same visual language

## Nusantara-AI house rules
- Public brand is `NUSANTARA-AI NEWS`.
- Keep writing in Jaksel/Gen-Z style, but stay KBBI-friendly.
- Never show visible source labels/names in the public asset or caption.
- For each generated story, emit both a 4:5 Instagram image and a short video.
- Every short video must visibly carry the news title / hook in-frame.
- Telegram sends should be gated on file existence:
  - do not send an image if the rendered PNG is missing
  - do not send a video if the video asset or reference image is missing
  - prefer a clear skip reason over a partial send
- Before sending to a specific Telegram destination, inspect the available targets and confirm the exact channel/chat mapping. Do not assume bare `telegram` is the intended public channel; it may resolve to the home channel or a mirrored destination.
- For "tinggal copas" requests, output one Markdown block per item with title, caption, CTA URL on its own line, hashtag line, and media path line.
- Final runs should end with a completion report only after all enabled stages finish.

## Core inputs
- Source script: `/root/nusantara-ai-saas/scripts/genz-news.ts`
- Default template for the flyer workflow: `/root/nusantara-ai-saas/templates/bot_template.html`
- Gen-Z template override for the flyer workflow: `/root/nusantara-ai-saas/templates/bot_template.html` via `--template` when that clean 4:5 layout is desired
- Use `scripts/prompt-to-images.ts` for Instagram image generation and `scripts/images-to-video.ts` for Shorts; pass the Instagram image URL as the video reference image.
- The public news brand is `NUSANTARA-AI NEWS` and the visible output must never show source labels/names.
- Output dir: `/root/nusantara-ai-saas/data/genz-news/<run-timestamp>/`
- Flyer pack requests that say `1 file flyer berikut caption dan 4 hashtag` should be split into one Markdown file per flyer in a dedicated folder. Each file should include the flyer path, caption, exact CTA URL if the user provided one, and exactly 4 hashtags. See `references/flyer-caption-pack.md`.
- Env vars:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`
  - `ARK_API_KEY` (or `BYTEDANCE_API_KEY` / `BYTEPLUS_API_KEY` alias)
  - `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` for Shorts upload
  - optional registry override: `DAFTAR_API_LOKAL_INDONESIA_URL`

See `references/genz-template-notes.md` for the current template selectors and headline-fit rules.
See `references/news-source-registry.md` for the older registry-backed news source notes and endpoint quirks.
See `references/news-source-registry-and-delivery.md` for the current source-order, dry-run, and retry notes discovered in the latest run.
See `references/source-registry-and-lexical-scoring.md` for section-based registry extraction and KBBI scoring notes.
See `references/session-2026-05-07-source-registry-and-kbbi.md` for the latest local-repo integration notes and verification checklist.
See `references/session-2026-05-07-video-title-kbbi.md` for the MP4 title overlay and caption-format update.
See `references/headline-title-case.md` for the cleaned-title case, acronym preservation, and boundary-aware truncation rules.
See `references/nusantara-ai-news-pack.md` for the current brand rules, 4:5 + short-video dual output convention, no-source-public-output rule, and final report expectations.
See `references/news-pipeline.md` for the full generate → Instagram 5:4 → short video → YouTube → Telegram orchestration notes, including caption hooks and final report formatting.
See `references/news-pipeline-image-first.md` for the image-first Instagram → video reference flow and the `referenceImageUrl` reporting convention.

Do not hardcode or repeat secrets in chat or logs.

## Workflow
1. Make sure the template points to the clean layout.
   - No purple sidebar on the left.
   - No visible description line under the title.
   - Keep the title readable; do not over-truncate it to the point of ugly ellipses.
2. Use the generator script to collect ranked news candidates.
   - Keep the banned-topic filter active.
   - Prioritize current, clickable, safe items.
   - If the user wants a new local source repo installed into automation, clone it under `/root/.hermes/vendor/`, then wire it into the generator as a read-only snapshot or fallback source rather than hardcoding URLs in the skill.
   - For registry-style repos, prefer section parsing from README headings plus a per-run JSON snapshot so future runs are reproducible.
3. Render all 10 items using Seedream via ARK.
   - Use the image-generation path already in the script.
   - Keep prompts clean: no text, logo, watermark, or UI.
   - If the workflow also needs short video outputs, first finish news selection/rendering, then run `npm run gen:viral-news:video-titles` to burn the title onto each MP4 and keep a per-item retry path.
   - For 4:5 delivery, pass `--aspect 4:5` and keep `--template /root/nusantara-ai-saas/templates/bot_template.html`; verify the output dimensions before sending.
   - When a local repo is being added as a source dependency, prefer a read-only vendor snapshot plus a per-run manifest artifact over hardcoding live URLs in the skill.
4. Generate one caption per PNG.
   - Include `Judul:` and `Inti cerita:` lines.
   - Add a short CTA.
   - Append hashtags.
5. Send each PNG to Telegram with caption.
   - For media packs, verify delivery item-by-item when possible so one failure does not block the entire batch.
- Verify the run by checking the manifest, one sample 4:5 image, and one sample final short video if needed.
7. If a title clips in the PNG, fix the template and headline-fit logic before rerunning the full batch.
8. If a single media task fails, retry only that item with a simpler prompt or the same source asset before considering a full rerun.

## Template/layout notes
- See `references/template-cleaning-and-title-fit.md` for the clean baseline and verification recipe.
See `references/video-5x4-genz-template.md` for the 5:4 `genz.html` video export and verification notes.
See `references/source-discovery-without-instagram.md` for the session-specific fallback when Instagram profile pages are login-gated or rate-limited.
See `references/feed-design-rendering.md` for the single-feed 4:5 SVG/ffmpeg workflow and the no-watermark verification checklist.
See `references/session-2026-05-07-telegram-target-mapping-and-copy-paste.md` for the per-item Telegram copy format and the rule to verify the exact destination before sending.

## Deduplication
- Load `data/genz-news/history.json` before ranking candidates.
- Reject stories that match on canonical key, normalized title, compact title, or strong content overlap.
- Apply the duplicate filter before ranking so old stories do not take a final slot.
- Persist the `key` field back into history for every published item.
- Do not depend on source URL alone; different sources often republish the same story with a new link.

## Recommended command
From `/root/nusantara-ai-saas`:

```bash
TELEGRAM_BOT_TOKEN="<set in env>" \
TELEGRAM_CHAT_ID="<set in env>" \
ARK_API_KEY="<set in env>" \
npm run gen:viral-news -- --count 10
```

Use `--dry-run` when you only want the files and manifest, not Telegram delivery.

## Caption format
Use this structure:

- `Judul: ...`
- `Hook viral: ...`
- `Inti cerita: ...`
- blank line
- short CTA
- blank line
- hashtags

For Telegram-ready packs, keep the CTA as a plain URL on its own line when the user wants a copy/paste block.
Keep the wording natural Indonesian: Gen-Z feel is fine, but prefer KBBI-friendly phrasing over slang yang terlalu liar.
Always include `#HookViral` in the hashtag block.
Do not add visible source attribution in the public caption or asset.

## Visual rules
- One PNG per article
- Clean composition
- Short headline only
- No lower description text
- No purple vertical bar on the left
- Premium dark template is preferred
- Gen-Z styling is preferred for this workflow: modern font, higher-contrast neon accents, and a darker but livelier blue/purple palette.
- Make the card visually consistent across all 10 items
- For feed-only requests, keep the final asset free of visible source labels, watermark text, or technical footer text.
- When using an external/provider image, crop or reframe it so embedded source overlays do not survive into the final PNG.

## Headline handling
- Keep card headlines short, but do **not** cut through the middle of a clause or sentence.
- Normalize the raw feed title first: strip prefixes like `Foto:` / `Breaking:`, convert to readable title case, and preserve acronyms like `OJK`, `SDM`, or `QRIS`.
- Prefer the full cleaned title first, then shorten by word boundary if needed; avoid hard-slicing characters when a clean phrase is available.
- If the title is still long, remove trailing context words rather than trimming in the middle of a clause.
- The current generator logic uses `normalizeNewsTitle()`, `smartTruncateText()`, and `buildCardHeadline()`; keep them aligned with the template size.

See `references/genz-template-notes.md` for the current template and title behavior notes.

## Verification
After the run, verify:
- the run folder exists under `data/genz-news/`
- `manifest.md` exists and includes caption + hashtags
- Telegram send logs show all 10 documents sent
- at least one sample PNG looks clean:
  - no left purple sidebar
  - no visible summary line below the headline
  - title is short and readable

See `references/telegram-delivery.md` for the retry pattern when Telegram rate limits a media send.

## Pitfalls
- Never expose the real bot token or ARK key in chat or final output.
- If Telegram env vars are missing, stop and ask for them or run `--dry-run`.
- If image/video generation credentials are missing (for example the image tool reports `FAL_KEY environment variable not set`), do not claim a new render; use `--dry-run` or reuse a verified existing asset only if it is present on disk.
- Do not assume `target: "telegram"` in the messaging tool means the user’s intended public channel. Verify targets with the target-list tool first; otherwise you may send to the home channel or a mirror instead of the requested destination.
- If the generator already rendered files but Telegram delivery is blocked, the outputs are still usable; send the PNGs manually with the Telegram send tool if available.
- If the provider is slow, let the batch finish; do not interrupt early.
- If Telegram sends hit flood control, wait and resend only the failed media item instead of restarting the entire batch.
- If the layout regresses, patch `/root/bot_template.html` instead of editing generated output.
- For MP4 title overlays, keep the ffmpeg `drawtext` filter minimal; stray notes/text inside the filter string will break rendering.
- If the Shorts output must carry audio, regenerate the MP4 with an audio stream and verify it with `ffprobe -select_streams a:0` before upload or Telegram delivery.
- Keep the banned-topic filter intact so religion, politics, and sexual stories are excluded.
- When improving selection quality, treat KBBI/dictionary coverage as a soft signal; do not let it dominate relevance or freshness.
- After changing sources or scoring, run a dry-run and verify the manifest includes the registry snapshot and source metadata before sending the full batch.
- After changing dedup logic, verify that a repeat run skips already-published items rather than filling the batch with near-duplicates.
