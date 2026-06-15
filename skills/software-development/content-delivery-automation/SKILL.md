---
name: content-delivery-automation
description: Build and run on-demand content pipelines that fetch source material, filter/reshape it, render branded assets, and deliver the results to chat platforms like Telegram.
---

# Content Delivery Automation

Use this skill for on-demand automation that turns external content into generated assets and sends them to a destination channel/app.

Typical shape:
1. Collect candidate content from approved sources.
2. Filter out disallowed or off-brand items.
3. Rewrite or summarize into the target voice.
4. Render the result into a branded image/video/template.
5. Deliver the files one-by-one to Telegram or another chat endpoint.

## Start here
- Confirm the destination channel and whether delivery is manual/on-demand or scheduled.
- Confirm the source types and exclusions up front.
- Confirm the template path and output format before coding.
- If the source arrives as a zip/archive, inspect it first and extract it with a safe tool available in the environment.
- Keep secrets only in env vars or secret storage. Never hardcode or echo tokens.
- If the user explicitly says not to use APIs for content generation, keep the pipeline local/manual: reuse existing assets or render from local files, avoid provider calls, and only perform non-generative delivery steps.

See `references/news-image-telegram-pipeline.md` for a concrete session pattern covering zip intake, HTML-template inspection, PNG rendering fallback, and Telegram send verification.

See `references/seedream-byteplus-telegram.md` for the Seedream/Byteplus ARK image path, watermark-off generation, JPEG-to-PNG conversion, and Telegram delivery notes.

See `references/news-viral-packaging.md` for the 10-card viral news pipeline: shortlist, taboo-topic filtering, debate/vote ranking, Gen-Z rewrite, and one-PNG-per-item packaging.

See `references/genz-news-byteplus-pipeline.md` for the session-proven Gen-Z viral pack workflow: debate/vote shortlist, distinct hooks per card, BytePlus ARK Seedream generation, PNG packaging, manifest output, and dry-run strategy.

See `references/nusantara-ai-news-pipeline.md` for the latest Nusantara-AI News pipeline notes: public brand rules, hidden source policy, 5:4 Instagram image output, headline-mandatory short videos, image-first reference flow, and the `ark:prompt-to-images` / `ark:images-to-video` helpers.

See `references/nusantara-ai-news-image-first.md` for the latest image-first news automation notes: image-before-video sequencing, OpenAI/ARK provider switch, 5:4 Instagram deliverable, 30s Shorts floor, and host-based news subdomain routing.

See `references/youtube-shorts-pipeline.md` for the manifest-driven YouTube Shorts upload flow, dry-run short-circuit pitfall, OAuth env shape, and 9:16 renderer notes.

See `references/news-indo-api-next.md` for the Berita Indo API Next route map, payload shapes, filtering notes, and the template mismatch pitfall observed in session.

See `references/genz-news-debate-voting-backtest.md` for the Berita Indo multi-source shortlist workflow, vote/backtest scoring recipe, `#slide` render-anchor pitfall, and dry-run verification notes.

See `references/genz-news-telegram-session-2026-05-06.md` for the latest Telegram delivery notes, cleaner template tweaks, caption schema (`Hook:` / `Viral momentum:`), and secret-handling pitfall captured from the live rerun.

## News-source extraction
- Use this when the pipeline starts from a news feed or article search rather than from already-clean source text.
- Normalize headline, link, image, and body fields before rewriting.
- Fall back to page scraping if the helper API is broken or missing.
- See `references/news-feed-extraction.md` for the condensed extraction checklist.

## Recommended workflow
1. Inspect the template and the existing repo structure.
2. Build a deterministic content-selection stage first.
3. Add a strict filter stage for taboo topics and low-signal content.
4. Generate rewritten copy in the requested tone.
5. Render the template to the final asset format.
6. Add the delivery step last, after the assets are reproducible locally.
7. Verify end-to-end with a dry-run before sending real messages.

## Filtering and rewriting
- Implement source allowlists and topic deny-lists separately.
- Prefer explicit keyword/topic filters plus a final relevance check.
- When the user asks for a shortlist of current items, rank first on freshness + visual punch + shareability, then do a quick debate/vote if the top candidates are close.
- When the user wants a specific audience style, rewrite only after filtering.
- If the user asks to omit source labels from the final asset, remove source labels from the rendered template too.
- If the user asks to omit source labels from the final asset, remove source labels from the rendered template too.
- For Nusantara-AI news outputs, use `NUSANTARA-AI NEWS` branding, keep Jaksel/Gen-Z phrasing KBBI-friendly, and do not show source labels in the public asset or caption.
- Keep flyer copy varied across cards; avoid repeating the same lead phrase, hook pattern, or filler word across the pack.

## Rendering
- Prefer source template files over generated build artifacts.
- When the user names a specific template file (for example `genz.html`), inspect the actual file before wiring any data, and verify it contains the expected render anchor (for example `#news-card`). A spec sheet or prompt guide is not the same thing as a screenshot-ready template.
- In one session, `/root/genz.html` was a spec-style guide and `/root/template.html` was the working screenshot template; choose the file by DOM structure, not by filename alone.
- For news cards, keep the top/hero text extremely short when requested: 1–3 words is a good default for the visible title badge.
- If the user asks for a cleaner composition, remove decorative sidebars/accent bars and hide any under-title description block in the template instead of only shrinking the text.
- If the user asks for a cleaner composition, remove decorative sidebars/accent bars and hide any under-title description block in the template instead of only shrinking the text.
- If the user asks to remove source attribution, omit source labels from the rendered image rather than only hiding them in upstream data.
- Use article images or page OG images when available; otherwise fall back to a topic-matched generated illustration or symbol so the card still feels grounded in the news item.
- For HTML-to-image rendering, use a repeatable browser path and verify the output dimensions/aspect ratio.
- For Nusantara-AI News, the Instagram image deliverable should follow the requested feed ratio (commonly `4:5`; some legacy runs may still show `5:4`) and the video deliverable should keep the headline visibly embedded in the final frame.
- If the browser screenshot step waits for a selector that never appears, inspect the template root first; a missing anchor usually means the wrong HTML file was chosen rather than a transient browser failure.
- If browser installation fails in the environment, look for a system Chromium/Chrome executable before changing the pipeline.
- If the browser-based rendering is unavailable or times out on local HTML/data URLs, switch to a deterministic CLI renderer rather than retrying indefinitely.
- For hero-image templates, prefer centering and slight upscaling of the image slot over shrinking the image when the composition feels bottom-heavy.
- If generated cards need a topical image but the template has no image slot, create a generated illustration that matches the topic and place it into the composition before the render.
- When using BytePlus/ARK image generation, set `watermark: false` at generation time; do not try to hide it only after the fact. Some ARK image models return a JPEG URL even when the final deliverable should be PNG, so download first and transcode locally before Telegram upload.
- For batch-style news packs, use a short caption schema that keeps the user-facing hook and the viral momentum distinct (for example `Hook:` and `Viral momentum:`), then append a CTA and hashtags. Keep the hook short and varied so the same opener does not repeat across the pack.
- If the request is to "select the most viral" from a larger set, rank by freshness + shareability + visual punch first, then do a lightweight debate/vote among the close top candidates before rendering.

## Packaging and manifests
- Keep one visual asset per item: 1 PNG per story/card.
- Write a human-readable `manifest.md` that maps each PNG to title, hook, caption, hashtags, and source.
- For news packs, keep captions and hashtags as separate fields so they can be reused for Telegram or other channels.
- When sending to Telegram, use `sendDocument` if the PNG must remain exact; send sequentially when the user wants per-item delivery.
- When targeting YouTube Shorts, drive uploads from a manifest that already points to the rendered video file, and record per-item upload status in a separate `youtube-upload-manifest.json`.
- Do not echo or restate pasted bot tokens/chat IDs in the reply; treat them as secrets and only verify presence via masked env checks.
- When the user asks for a viral shortlist, dry-run 1 item first, then scale to the final batch after checking layout and tone.
- Long batch jobs should use explicit timeouts on fetch/generate/download steps so they fail fast instead of hanging.

## Telegram delivery
- Send files one at a time when the user explicitly wants sequential delivery.
- Use `sendDocument` when the exact PNG/file must be preserved; use `sendPhoto` when inline preview matters more.
- For news pipelines that produce both image and video, send the image first with `sendDocument`, then the video with `sendVideo`, and skip only when one of the files is missing. See `references/news-telegram-paired-delivery.md`.
- Keep bot tokens and chat IDs in env/config, not in chat logs or source.
- If a bot token was exposed in chat, recommend rotating it before using it again.
- Verify send-file behavior with a small dry-run or a single test asset before dispatching the full batch.

## Pitfalls
- Source feeds can include off-topic listicle pages, galleries, audio stories, polls, lowongan, or promotional pages; filter them out early.
- Public-facing copy can accidentally leak internal labels or source names if you reuse raw titles directly.
- Playwright browser downloads may fail in restricted environments; a system Chromium binary can be a practical fallback.
- `browser_navigate` / browser-file rendering can time out on local HTML or data URLs; if that happens, switch to a terminal-based render path instead of retrying indefinitely.
- Do not assume the template has all required slots; inspect the actual HTML before wiring data.
- Do not treat a successful render as a successful delivery; verify the chat upload separately.
- When generating narration for a video pipeline, use a presenter-style opening in clean Indonesian and avoid passing ellipsized/truncated summary fragments straight into TTS.

## Verification
- Dry-run selection count
- filter hit list / excluded items
- final rewritten text sample
- rendered asset dimensions and file count
- visual check for clipping, watermark, and obvious artifacts
- Telegram send success for at least one file

## Support files
- See `references/news-image-telegram-pipeline.md` for the session pattern: source filtering, Gen-Z rewrite, HTML-to-PNG render, Chromium fallback, and sequential Telegram send notes.
- See `references/genz-news-byteplus-pipeline.md` for the session-proven Gen-Z viral pack workflow: debate/vote shortlist, distinct hooks per card, BytePlus ARK Seedream generation, PNG packaging, manifest output, and dry-run strategy.
- See `references/news-indo-api-next.md` for the Berita Indo API Next route map and template mismatch pitfall.
- See `references/article-generator-backend-pipeline.md` for the safe Article Generator API backend pipeline, env loading order, admin route shape, and local draft storage notes.
