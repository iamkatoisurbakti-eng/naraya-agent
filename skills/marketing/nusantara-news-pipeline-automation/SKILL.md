---
name: nusantara-news-pipeline-automation
description: End-to-end automation for Nusantara-AI News generation, configurable Instagram feed images (default/requested 4:5), 9:16 YouTube Shorts video, public article publishing, and Telegram delivery.
---

# Nusantara-AI News Pipeline Automation

Use this skill when the user asks to run, modify, or troubleshoot the full Nusantara-AI News pipeline.

## Scope

This pipeline produces, per news item:
- 1 configurable feed image for Instagram (`NEWS_INSTAGRAM_ASPECT`, commonly `4:5`; older runs may show `5:4`)
- 1 video short 9:16 with minimum HD 1080x1920
- public article/page output for news.nusantara-ai.online; generation should be explicitly reported as `post-news-platform` when `NEWS_ARTICLE_AUTOPOST=1` (default)
- Telegram delivery after both image and final video exist
- optional YouTube Shorts upload
- optional Facebook Page photo post via Meta Graph API (`NEWS_FACEBOOK_AUTOPOST=1`, `META_PAGE_ID`, `META_PAGE_ACCESS_TOKEN`)

## Core files

- `/root/nusantara-ai-saas/scripts/genz-news.ts`
- `/root/nusantara-ai-saas/scripts/news-pipeline.ts`
- `/root/nusantara-ai-saas/scripts/images-to-video.ts`
- `/root/nusantara-ai-saas/scripts/prompt-to-images.ts`
- `/root/nusantara-ai-saas/scripts/genz-news-video-title.ts`
- Prompt-enhancer note: `references/openai-prompt-enhancer.md`
- Session note: `references/session-2026-05-08-openai-flyer-prompt-enhancer-and-provider-gates.md`
- Batch-mode note for 5 flyer + 5 short runs: `references/session-2026-05-08-5x-flyer-short-automation.md`
- Telegram caption + frame fallback note: `references/session-2026-05-08-telegram-caption-plus-frame-fallback.md`
- Limit-mapping note for GPT-4o + Seedream/Seedance automation: `references/session-2026-05-08-gpt4o-seedream-seedance-limits.md`
- Shorts overlay browser fallback: `references/session-2026-05-08-shorts-overlay-browser-fallback.md`
- OpenAI one-off fallback for 1 flyer + 1 short: `references/session-2026-05-08-openai-oneoff-1flyer-1short-fallback.md`
- Sora Shorts scene-splitting reference: `references/sora-shorts-scene-splitting.md`
- `/root/nusantara-ai-saas/scripts/youtube-shorts-upload.ts`
- `/root/nusantara-ai-saas/scripts/byteplus-docs-index.mjs`
- `/root/nusantara-ai-saas/config/byteplus-ark-automation.json`
- `/root/nusantara-ai-saas/src/services/news-articles.ts`
- Reference notes:
  - `/root/.hermes/skills/marketing/nusantara-news-pipeline-automation/references/byteplus-ark-byte1-byte14-automation.md`
  - `/root/.hermes/skills/marketing/nusantara-news-pipeline-automation/references/openai-gpt-image-2-provider.md`
  - `/root/.hermes/skills/marketing/nusantara-news-pipeline-automation/references/rotate-image-provider.md`
- `/root/.hermes/skills/marketing/nusantara-news-pipeline-automation/references/session-2026-05-08-cron-reset-verification.md`
- `/root/.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.
- `/root/.hermes/skills/marketing/nusantara-news-pipeline-automation/references/session-2026-05-08-cron-reset-verification.md`
- `/root/.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall./root/.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.

- `/root/.hermes/skills/marketing/nusantara-news-pipeline-automation/references/session-2026-05-08-cron-reset-verification.md`
- `/root/.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.

- `/root/.hermes/skills/marketing/nusantara-news-pipeline-automation/references/session-2026-05-08-cron-reset-verification.md`
- `/root/.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.rmes/ski`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.ot/.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.rmes/ski`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall./.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.`/root/.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall..h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall./root/.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.on.md`
- `/root/.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.es/ski`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.es/ski`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall./ski`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.s/ski`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall./root/.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.

  - `/root/.hermes/skills/marketing/hermes-agent-orchestration/references/session-2026-05-07-visual-audio-qc-agent-chain.md`
- `/root/nusantara-ai-saas/src/services/news-articles.ts`
- `/root/nusantara-ai-saas/src/routes/news.ts`
- `/root/nusantara-ai-saas/templates/bot_template.html`
- HTML export helper: `scripts/render-html-to-png.mjs`
- Example-to-Shorts reference: `references/session-2026-05-07-shorts-template-from-example.md`
- News-card prompting reference: `references/news-card-prompting.md`
- Detik + CNN news-pack workflow: `references/news-pack-detik-cnn.md`
- Instagram 4:5 template: `/root/nusantara-ai-saas/templates/bot_template.html`
- Fallback note for blocked live generation and reusable assets: `references/session-2026-05-07-media-generation-fallback.md`
- Session note for provider failures and fallback reuse: `references/session-2026-05-08-fallback-reuse-and-provider-failures.md`
- `/root/.hermes/skills/marketing/nusantara-news-pipeline-automation/references/session-2026-05-08-cron-reset-verification.md`
- `/root/.h`
- See `references/flyer-single-render.md` for the one-flyer render/verification flow and the Telegram-env nonzero-exit pitfall.
- See `references/html-to-png-render-and-layout-overlap.md` for the Playwright HTML→PNG export flow and the common "font looks broken" layout-overlap pitfall.
- See `references/html-to-png-render-and-layout-overlap.md` for the Playwright HTML→PNG export flow and the common "font looks broken" layout-overlap pitfall.

## Working rules

- Keep all credentials in env/files only; never print real secrets.
- User authorizes direct production-focused edits in `/root/nusantara-ai-saas` when evaluation/scoring is 90+: change source/platform behavior, deploy/restart when needed, and verify live behavior before claiming success. Still avoid destructive actions and never expose secrets.
- `.env.example` must be a placeholder-only template: before/after editing it, scan for secret patterns (`ark-`, `sk-`, Telegram bot token, `GOCSPX-`, `cfat_`) and immediately blank any real-looking values. Actual secrets belong only in `.env`/deployment env, never in examples or final responses.
- Use `NUSANTARA-AI NEWS` branding in public-facing output.
- Do not show source labels in public news output.
- Keep image-first flow:
  1. Generate Instagram/feed image using `NEWS_INSTAGRAM_ASPECT` (use numeric ratio such as `4:5`)
  2. The generated image must be a concrete event/behavior scene related to the news, not a text poster and not a reporter/news-anchor/newsroom shot. Keep `NEWS_IMAGE_EVENT_SCENE_ONLY=1` unless explicitly debugging.
  3. Keep visual seed, center framing, and overlay safe-zone guards enabled: `NEWS_VISUAL_SEED=24857`, `NEWS_VISUAL_CENTERING_GUARD=1`, and `NEWS_VISUAL_OVERLAY_SAFE_ZONE=1`. Derive a stable per-story seed and pass it to both image and video stages so style/composition stays consistent. Prompts must require center-safe, medium-wide framing with 10–15% margin and no cropped subjects; important subjects/actions must stay in the upper/middle safe area while the lower 30–35% stays simple/low-detail so title/CTA overlays never collide with faces, vehicles, buildings, or key evidence. Templates must use `object-fit: contain` + `object-position: center center` and reserve a separate dark title area.
  4. Current requested video mode is text-to-video prompt only: keep `NEWS_VIDEO_USE_REFERENCE_IMAGE=0` so the 9:16 video does not use the Instagram 4:5 image as a reference. Raw footage should be generated from the news prompt directly and show actions/behavior/context from the event, not a presenter speaking to camera. Only set `NEWS_VIDEO_USE_REFERENCE_IMAGE=1` if the user explicitly asks to reuse the Instagram image as reference.
  5. Overlay title on final video if needed
- If provider credentials are missing or the image tool fails with `FAL_KEY environment variable not set`, stop claiming a fresh render and fall back to existing assets under `data/genz-news/**` or to ready-to-run commands/prompt templates.
- If prompt enhancement or provider generation fails with `401`, `403`, or `InvalidEndpointOrModel.NotFound`, treat it as a provider/prompt-layer failure; continue with the raw prompt when possible, but do not claim a fresh render unless an actual image/video file was produced. If reuse is acceptable for the slot, mark the run/report clearly as `fallback-reuse` and verify the reused PNG/MP4 on disk before Telegram send.

- Agent workflow defaults:
  - Content Ideation Agent generates trend-aware Shorts ideas and passes structured ideas to Script Writing Agent.
  - Script Writing Agent outputs title, hook, narration text, CTA, visual direction, estimated duration, and hashtags; narration text may be used for captions/scripts, but should not imply OpenAI TTS is active.
  - Before Visual & Audio Creation Agent or publication, normalize every script/naskah handoff to Bahasa Indonesia baku/KBBI style. Use the repo NLP helpers in `/root/nusantara-ai-saas/src/services/indonesian-nlp.ts`: `normalizeIndonesianScriptPacket` for agent handoffs, `normalizeIndonesianFormalText` for titles/summaries/article text, and `normalizeIndonesianMultilineText` for captions so line breaks are preserved. See `references/session-2026-05-07-kbbi-nlp-normalization.md`.
  - Visual & Audio Creation Agent converts the script into SEEDANCE text-to-video production prompts/payloads with generated-video ambience/action audio only. When filtering visual/audio prompts, filter the positive/public prompt text only; keep `negative_prompt` separate because it intentionally contains disallowed concepts as exclusions. See `visual-audio-creation-agent/references/session-2026-05-07-visual-audio-agent-setup.md`.
  - See `references/session-2026-05-07-agent-workflow-seedance-no-openai-tts.md` for the concise session-specific spec.

- Video defaults:
  - ratio: `9:16`
  - minimum resolution: `1080x1920` HD
  - cinematic realism/action enabled by default: `NEWS_VIDEO_CINEMATIC_REALISM=1`, `NEWS_VIDEO_CRF=14`, `NEWS_VIDEO_BITRATE=16M`, `NEWS_VIDEO_BUFSIZE=32M`; prompts should request cinematic realist Indonesian news documentary with realistic action / bioskop-quality footage, filmic lighting, natural color grade, HDR, stable real-world motion, realistic anatomy, credible action/ambience, and explicitly avoid CGI/cartoon/plastic/glitch/jitter visuals.
  - scene duration: `4s`
  - scene count: `5`
  - total target duration: `15–20s` preferred for Shorts; never exceed `20s` unless the user explicitly asks for a longer cut
  - copyright-safe mode enabled by default: `NEWS_COPYRIGHT_SAFE_MODE=1`. Prompts must require original/generated visuals and audio, avoid copying/imitating TV/movie/social clips, stock footage, famous photos/artwork, music, melodies, logos, trademarks, fictional characters, celebrities as impersonation, platform UI, and watermarked media. Use generic/fictitious realistic people/locations/props. This reduces Content ID/copyright risk but is not a legal guarantee.
  - Provider/output watermarks must stay disabled by default: `NEWS_WATERMARK=0`, `NEWS_IMAGE_WATERMARK=0`, and `NEWS_VIDEO_WATERMARK=0`. Pass `--watermark=false` or env-driven false to image/video provider calls; never enable provider watermarks unless the user explicitly asks.
  - Running text/ticker/subtitle/crawl must stay disabled by default: `NEWS_NO_RUNNING_TEXT=1` and `NEWS_VIDEO_NO_RUNNING_TEXT=1`. Raw/generated footage must contain no readable text, no ticker, no subtitles/captions, no lower-third motion, no marquee/crawl, and no animated text. Public text should be limited to the static Nusantara-AI News overlay/title/CTA template only.
  - Text-to-video no-reference mode is active by default for Shorts: `NEWS_VIDEO_USE_REFERENCE_IMAGE=0`. The pipeline may still generate the Instagram 4:5 image for Telegram/Facebook/news assets, but the video stage must not pass that image as `--image-url`; it should generate cinematic realistic action footage directly from the news prompt. Use `NEWS_VIDEO_USE_REFERENCE_IMAGE=1` only on explicit request.
  - OpenAI TTS/natural presenter narration is disabled by current user request: keep `NEWS_NATURAL_NARRATION=0` and `NEWS_TTS_PROVIDER=disabled`. Do not call `/audio/speech`, do not require `OPENAI_API_KEY` for narration, and do not run `scripts/news-video-natural-narration.ts` unless the user explicitly asks to re-enable TTS. Current audio policy is generated-video audio only: keep `NEWS_TTS_ONLY_AUDIO=0`, `NEWS_GENERATED_VIDEO_AUDIO_ENABLED=1`, `NEWS_GENERATED_VIDEO_AUDIO_VOLUME=1.00`, `NEWS_NARRATION_VOLUME=0`, `NEWS_BACKSOUND_ENABLED=0`, and `NEWS_BACKSOUND_DUCKING=0`. The video generator should create copyright-safe original cinematic action/ambience audio, with no dialog/voice-over/music imitation.
- Use digital character, template, or element only when relevant; do not force them on every video.
- If the user wants GPT-4o to refine the flyer prompt first, use the OpenAI prompt-enhancement path (`NEWS_FLYER_PROMPT_PROVIDER=openai`, `NEWS_FLYER_PROMPT_MODEL=gpt-4o`) before the image provider runs; see `references/openai-prompt-enhancer.md`. If that enhancer returns 401/403 or throws, treat it as a non-fatal quality-layer failure: log a warning and continue with the raw prompt instead of stopping the pipeline. See `references/session-2026-05-08-openai-prompt-enhancer-fallback.md`. If the user asks for GPT Images 2.0, set image generation only to OpenAI with `NEWS_IMAGE_PROVIDER=openai`, `IMAGE_PROVIDER=openai`, and `OPENAI_IMAGE_MODEL=gpt-image-2`, while keeping `NEWS_NATURAL_NARRATION=0` and `NEWS_TTS_PROVIDER=disabled`. If the user explicitly asks for Seedream 4.0 / BytePlus image generation, use the Ark/BytePlus path with model `seedream-4-0-250828`; see `references/seedream-4-0-image-batch.md`. Real `gpt-image-2` calls may fail with OpenAI org-verification HTTP 403; see `references/openai-gpt-image-2-provider.md` and do not claim a real render until it succeeds.
- If rotation is enabled, alternate Ark and OpenAI across items and verify the manifest `provider` field alternates as expected.
- Keep video generation on Ark by default as well; the video stage already uses Ark/Byteplus task submission.
- If rotation is intentionally enabled, verify the runtime container actually received the env override before assuming rotation is live.
- When running a single-news mode (`--count 1` / one-item mode), require score 95+ and fail early if no candidate clears the threshold. In the pipeline, read the score from the generated news manifest before creating prompt/image/video assets.
- When sending to Telegram, require the relevant files to exist first:
  - image send requires the rendered image file
  - video send requires both reference image and final video file
  - skip the item with a clear reason instead of sending partial media
  - do not claim Telegram success until the Telegram API call succeeds and `pipeline-report.json` marks the item sent
- If the user asks for `run now`, don’t assume `cronjob run` is enough. Verify whether it actually executes the pipeline or just schedules the next tick; if needed, call the real runner directly, then confirm files/logs/Telegram before claiming success.
- Prefer a daily all-in-one distribution job when the user wants one automation run for YouTube + article + Telegram + social-ready assets.
- Public Telegram mirroring is additive: `TELEGRAM_PUBLIC_CHAT_ID` / `TELEGRAM_PUBLIC_CHANNEL_NAME` can mirror the main delivery target without replacing it.
- Public Nusantara-AI News articles must read like real short news articles, not generic placeholders. Use concrete headings such as `Apa yang terjadi`, `Detail utama`, `Konteks dan dampak`, and `Yang perlu dipantau berikutnya`; never render visible source labels/buttons like `Buka sumber asli` on the public news UI. After changing article generation, sync `data/news-articles` into the Docker volume or redeploy plus copy the data so `https://news.nusantara-ai.online/api/news/articles` returns the updated article JSON.
- If the user asks for Instagram/TikTok posting, verify whether real uploader tooling exists before claiming publish success; otherwise output ready-to-post assets/captions and say so explicitly.
- When public article autoposting is enabled (`NEWS_ARTICLE_AUTOPOST=1`, default), treat `saveGeneratedNewsArticles` output as a first-class distribution step: verify `data/news-articles/index.json`, add/report a `post-news-platform` step, include `NEWS_PUBLIC_BASE_URL` article links in captions, and test a concrete public `https://news.nusantara-ai.online/news/...` URL with HTTP 200 before claiming success.
- If the user asks for Facebook Page posting, use the built-in Meta Graph API photo flow rather than treating a Business Manager link as sufficient. Require `META_PAGE_ID` and `META_PAGE_ACCESS_TOKEN`, store via `scripts/set-meta-page-secrets.sh`, and report only set/missing status.
- When the user asks for faster public access, prefer caching/CDN-style improvements over rotate proxy for public websites.
- If you need to answer a “coba hasilkan 1 flyer 1 video short sekarang” request but live media generation is blocked, reuse an existing matching PNG/MP4 pair from `data/genz-news/**` only if it is actually present and verified, and say clearly that it is a reused asset rather than a fresh render.

## Typical flow

1. Generate news items
   - command: `npm run gen:viral-news -- --count <n> --dry-run`
2. Generate 4:5 Instagram images
   - via `scripts/prompt-to-images.ts`
3. Generate short video directly from the text prompt (default no-reference mode; do not pass the Instagram image as `--image-url` unless `NEWS_VIDEO_USE_REFERENCE_IMAGE=1`)
   - via `scripts/images-to-video.ts`
4. Add title overlay if needed
   - via `scripts/genz-news-video-title.ts`
5. Upload YouTube Shorts when credentials exist
   - via `scripts/youtube-shorts-upload.ts`
6. Send to Telegram when enabled
7. Save article/page output
8. Write final pipeline report

## Selective creative hints

If needed, pass these only when relevant:
- `NEWS_VIDEO_DIGITAL_CHARACTER`
- `NEWS_VIDEO_TEMPLATE`
- `NEWS_VIDEO_ELEMENT`

These hints should be injected only if they improve the news visual.

## Verification checklist

Before telling the user it works, verify:
- generated image exists
- NLP/KBBI gate is active when requested: run `npm run test:unit -- --runTestsByPath tests/unit/indonesian-nlp.test.ts`, confirm `npm run build:server`, and inspect the dry-run `pipeline-report.json` so titles/captions/article links do not contain known informal tokens (`gak`, `nggak`, `guys`, `bgt`, `rame`, `bikin`, `subscribe`, `share`, `update`, `scroll`, etc.)
- generated image exists
- image/video generation dry-run shows seed propagation (`NEWS_VISUAL_SEED`, per-story seed, video scene seed = base + scene index)
- image and video prompts include center-safe framing rules when `NEWS_VISUAL_CENTERING_GUARD=1`
- template CSS keeps generated media centered/uncropped (`object-fit: contain`, `object-position: center center`)
- video exists and is 9:16
- video resolution is at least 1080x1920 HD
- video has audio when required
- article output exists in `data/news-articles` and the exact public `https://news.nusantara-ai.online/news/...` URL returns HTTP 200
- Telegram upload succeeded when enabled
- final report was written
- HTTPS/news host is reachable when deployment changed

Useful checks:
- `ffprobe` for width/height/duration/audio
- `curl -kfsSI https://news.nusantara-ai.online/news`
- `curl -kfsS https://news.nusantara-ai.online/news`

## Pitfalls

- Do not assume API key upload works for YouTube; Shorts upload needs OAuth 2.0 credentials.
- Do not accept `YOUTUBE_REFRESH_TOKEN=https://oauth2.googleapis.com/token` as valid; that is the OAuth token endpoint, not a refresh token. Generate an auth URL, have the user approve, exchange the returned code, then store the real refresh token without printing it. If Google says the app is still in Testing, add the user's Gmail/channel account under Google Cloud Auth Platform → Audience → Test users, then regenerate a fresh auth URL.
- Never leave real secrets in `.env.example`; if found, sanitize immediately and tell the user to rotate/regenerate the exposed keys/tokens.
- If an HTML template must be delivered as PNG, render it with Playwright/Chromium and verify the output with `file` before claiming success. For interactive video HTML, call `window.startVideo()` (or equivalent) before screenshotting if the first scene is hidden behind a preview overlay.
- If an MP4 render fails with `moov atom not found`, rebuild it from `video-frames.txt` using ffmpeg concat and then re-run `ffprobe`.
- Every flyer and Shorts item must include a *complete caption* and exactly 4 hashtags unless the user explicitly asks for a different count.
- Captions must not be truncated with ellipses or placeholder fragments; if a caption is produced, it should read as a finished publish-ready block.
- Use Indonesian dictionary/KBBI-style language for public content by default: `NEWS_LANGUAGE_DICTIONARY_MODE=kbbi` and `NEWS_CONTENT_LANGUAGE_STYLE=baku-indonesia`. Normalize slang/foreign casual words in titles, captions, article bodies, YouTube descriptions, and script/naskah handoffs before visual/video generation or any audio-producing stage (SEEDANCE audio prompts/ambience, or TTS only if user explicitly re-enables it). Examples: `gak/nggak`→`tidak`, `rame`→`ramai`, `bikin`→`membuat`, `kepo`→`ingin tahu`, `scroll`→`menggulir layar`, `subscribe`→`berlangganan`, `share`→`bagikan`, `update`→`pembaruan`, `gandeng/garap`→`menggandeng/menggarap`. Use `src/services/indonesian-nlp.ts` as the single reusable NLP layer and add/update unit tests in `tests/unit/indonesian-nlp.test.ts` whenever adding a replacement. For captions, do not run a whole-caption paragraph normalizer that destroys line breaks; use the multiline normalizer. Keep SEO hashtags/brand terms only where needed, but body content should read as clear Bahasa Indonesia.
- Keep anti-duplicate logic enabled using history, public article index, title normalization, and extended `NEWS_HISTORY_MAX_ITEMS` (default 240). If a 24-hour queue cannot find enough unique viral Gen-Z-safe stories, skip that slot (`no_unique_viral_news`) instead of forcing duplicates or low-score stories.
- Before sending to Telegram, confirm the rendered image file exists for the item.
- For video sends, confirm both the final image reference and final video file exist; skip the item if either asset is missing.
- HD 1080x1920 Shorts with narration can exceed Telegram Bot upload limits and trigger `Request Entity Too Large`. Before Telegram video send, check file size and compress/send a smaller Telegram preview variant using `NEWS_TELEGRAM_VIDEO_MAX_MB` (default 48) or skip Telegram video without failing the whole YouTube queue slot.
- If `overlay-video-title` reports `titled 0 videos` while `video-manifest.json` has succeeded items, inspect manifest field names. Pipeline raw manifests may use `rawVideoPath`; `scripts/genz-news-video-title.ts` must accept `rawVideoPath`/`titleVideoPath` as well as older `videoPath`/`filePath`.
- If a public Telegram mirror is configured, treat it as additive to the main delivery target and keep the skip-on-missing-media rule for every target.
- If screenshot verification fails, do not claim the article is public-ready yet; verify the JSON API first and fix the data sync or route before sending a report.
- For local HTML→PNG export with Chromium snap, `/snap/bin/chromium --headless --no-sandbox --disable-gpu --screenshot=... file:///...` can still work even when DBus/AppArmor accessibility warnings print. Treat those warnings as non-fatal unless the PNG is missing or unreadable. For interactive Shorts HTML, hide preview overlays or generate one static per-scene HTML variant per frame before screenshotting.
- For batch runs, verify that each of the 5 items has a complete caption and exactly 4 hashtags before marking the run done.
- `--dry-run` can still write/post public article records when `NEWS_ARTICLE_AUTOPOST=1`; switch that env to `0` for a fully local preview.
- If the public article JSON endpoint returns 404, check whether `data/news-articles` was synced into the running container volume before debugging the UI.
- When setting up scheduled YouTube uploads, verify OAuth readiness separately from normal Google Workspace/Gmail auth:
  - locate/validate the Desktop OAuth client JSON without printing `client_secret`
  - store `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` only in `.env`/environment
  - YouTube upload requires OAuth refresh token; API key or Gmail password is insufficient
  - `scripts/youtube-shorts-upload.ts` does not load `.env` itself; source `.env` or export the YouTube vars before running it directly.
- When a user requests hourly/24h YouTube queueing, use `gen:news-youtube-queue` rather than installing separate cron entries. For “24 jam 24 video 1 jam 1 video 1 artikel”, set/override `YOUTUBE_QUEUE_SLOTS=24`, `YOUTUBE_QUEUE_INTERVAL_SECONDS=3600`, `YOUTUBE_QUEUE_MONITOR_HOURS=24`, `YOUTUBE_UPLOAD_COUNT=1`, and `NEWS_ARTICLE_AUTOPOST=1`; stop any existing queue before starting the replacement to avoid double uploads. Keep the queue state/log files under `data/logs/`.
- When evaluating a 24h queue, separate runtime health from production-output health: poll the Hermes session/process tree for liveness and duplicate queues, then inspect `data/logs/youtube-hourly-queue.log` and `data/logs/youtube-hourly-queue-state.json` for slot outcomes. A running queue can still be operationally blocked if slot failures all come from provider errors. If logs show ARK/BytePlus HTTP 403 `AccountOverdueError`, diagnose it as a billing/provider blocker, not a code/YouTube/Telegram failure; report that future slots will likely fail until balance is fixed or fallback media generation is enabled. See `references/session-2026-05-07-24h-queue-evaluation-and-ark-overdue.md`.
- When the user says `startautomation` or asks to start the YouTube queue, run readiness gates before starting: check no duplicate queue process, verify YouTube OAuth is set, and verify ARK/BytePlus provider key exists. Do not require `OPENAI_API_KEY` while `NEWS_NATURAL_NARRATION=0` / `NEWS_TTS_PROVIDER=disabled`; require it only if the user explicitly re-enables OpenAI TTS narration. If required credentials are missing, do not start; set only non-secret defaults and report missing credentials.
- Before live-starting the queue, also validate `.env` syntax and repair common user-paste issues without exposing secrets. In particular, if a non-comment line looks like `TELEGRAMBOT:<bot-token>`, convert it to `TELEGRAM_BOT_TOKEN=<bot-token>` and re-run validation; otherwise do not start with malformed `.env` lines. If the user pastes a Meta/Facebook Business link as prose such as `facebook business meta : https://business.facebook.com/...`, normalize it to `META_BUSINESS_LINK="https://business.facebook.com/..."` and remove the malformed key. Quote `.env` values that contain spaces (notably `NEWS_TTS_CHARACTER` and `NEWS_END_CTA_SUBSCRIBE`) so both `dotenv` and shell sourcing work.
- For final live readiness, use safe probes that return only statuses: `npm run build:server`, YouTube OAuth refresh HTTP 200, Telegram `getMe` `ok: true`, and ARK/BytePlus readiness when media generation is needed. Do not run OpenAI model probes for TTS while TTS is disabled. Then start `scripts/run-youtube-hourly-queue.sh` in background and verify process/log/state files exist.
- When a user requests a scoring gate such as “below 90 jangan digunakan,” enforce it before image/video/upload generation with `NEWS_MIN_SCORE` and `NEWS_MIN_SINGLE_SCORE`, and verify the state/manifest records the threshold.
- If Instagram feed output aspect changes, use numeric `NEWS_INSTAGRAM_ASPECT` (e.g. `4:5`) and verify the manifest/output directory reflects it.
- If a single-prompt run fails the 95+ gate, stop before any image/video rendering rather than emitting a partial pipeline run.
- If the pipeline video stage throws a generic Ark `InternalServiceError`, try the direct fallback path with `scripts/images-to-video.ts` and the already-generated reference image URL before assuming the news item is unrecoverable.
- Do not rely on `--generate-audio false` to disable audio in `scripts/images-to-video.ts`; that flag is treated as a presence boolean. Omit the flag if you need silence.
- See `references/session-2026-05-07-video-stage-fallback-and-boolean-flag.md` for the exact fallback recipe and verification notes.

## Recommended commands

- Scheduled YouTube Shorts upload wrapper:
  - `npm run gen:news-youtube-upload -- --count 1`
  - Generates a news item, Instagram image, 9:16 Seedance prompt-only video with generated-video audio, and uploads to YouTube Shorts.
  - Default for YouTube schedule: `NEWS_MIN_SCORE=90`, `NEWS_MIN_SINGLE_SCORE=90`, `NEWS_INSTAGRAM_ASPECT=4:5`, `NEWS_NATURAL_NARRATION=0`, `NEWS_TTS_PROVIDER=disabled`, `NEWS_VIDEO_USE_REFERENCE_IMAGE=0`.
  - Skips Telegram by default; add `--send-telegram` only when paired Telegram delivery is desired.
  - Hourly 12-slot queue: `npm run gen:news-youtube-queue -- --slots 12 --interval-seconds 3600 --monitor-hours 24` or `scripts/run-youtube-hourly-queue.sh`.
  - If starting the runner with Telegram enabled, use `scripts/run-youtube-hourly-queue.sh --send-telegram` and verify the runner forwards `"$@"`; otherwise the log may show `sendTelegram:false` despite the shell arg.
  - YouTube Shorts audience/locale/growth defaults for this pipeline: `YOUTUBE_MADE_FOR_KIDS=0` (general/all-ages, not kids-only), `YOUTUBE_TARGET_COUNTRY=ID`, `YOUTUBE_DEFAULT_LANGUAGE=id`, `YOUTUBE_LOCATION_DESCRIPTION=Indonesia`, `YOUTUBE_CATEGORY_ID=25`, `YOUTUBE_GROWTH_MODE=1` / `NEWS_YOUTUBE_GROWTH_MODE=1`, and Indonesia-oriented growth tags (`ViralIndonesia`, `BeritaViral`, `NewsIndonesia`, `FYP`, etc.). Growth mode should remove internal source-file text from descriptions, include retention CTAs, article link when available, and subscribe/share prompts.
- YouTube OAuth helper: `npm run youtube:oauth -- --auth-url`, then exchange the returned browser redirect with `npm run youtube:oauth -- --code "http://localhost/?code=..."`.
  - Requires `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` in env; never hardcode OAuth secrets.
  - Install host cron daily at 07:00 with `YOUTUBE_UPLOAD_CRON="0 7 * * *" bash scripts/install-youtube-upload-cron.sh`.
- Telegram channel autopost wrapper:
  - `npm run gen:news-autopost -- --count 1`
  - default channel target: `@nusantaranewsindonesia` (`https://t.me/nusantaranewsindonesia`)
  - accepts `TELEGRAM_PUBLIC_CHANNEL_NAME`, `TELEGRAM_CHANNEL`, or `TELEGRAM_CHANNEL_URL`; `https://t.me/<handle>` is normalized to `@<handle>`
  - requires `TELEGRAM_BOT_TOKEN` and the bot must be admin in the target channel
  - install host cron every 6 hours with `NEWS_AUTOPOST_CRON="0 */6 * * *" bash scripts/install-autopost-cron.sh`
- For the user-owned hourly berita prompt-file workflow (`/root/.hermes/berita-daily.txt`), see `references/session-2026-05-08-berita-daily-hourly-telegram-export.md`.
- Dry-run pipeline:
  - `npm run gen:news-pipeline -- --count 1 --dry-run`
  - For the requested batch mode, use `npx tsx scripts/news-pipeline.ts --dry-run --count 5` to preview 5 flyers + 5 shorts.
  - For live batch runs, verify the run directory contains **5 flyer PNGs** and the video stage reaches `video-manifest.json` / `pipeline-report.json` before claiming success.
  - If the video model is unavailable or the provider returns `InvalidEndpointOrModel.NotFound` / `AccountOverdueError`, report the batch as blocked and do not call the run complete.
  - OpenAI TTS is currently disabled by user request; do not use this command unless the user explicitly re-enables TTS:
  - `npm run gen:news-video:natural-narration -- --video-manifest <video-title-manifest.json> --news-manifest <manifest.json>`
  - default env: `NEWS_NATURAL_NARRATION=0`, `NEWS_TTS_PROVIDER=disabled`, `NEWS_GENERATED_VIDEO_AUDIO_ENABLED=1`, `NEWS_GENERATED_VIDEO_AUDIO_VOLUME=1.00`, `NEWS_NARRATION_VOLUME=0`. Do not run OpenAI TTS unless the user explicitly re-enables narration.
  - current audio default: generated video audio only; no OpenAI `/audio/speech`, no TTS mix, no backsound.
  - end CTA default: `NEWS_END_CTA_SUBSCRIBE="Sebelum lanjut scroll, jangan lupa subscribe channel Nusantara-AI News, aktifkan loncengnya, dan bagikan video ini kalau menurut kamu penting."`
  - requires `OPENAI_API_KEY` for real TTS; dry-run without spending tokens: add `--dry-run`
  - Title/template precision convention:
  - Keep Shorts media locked to the template center-safe area: `NEWS_VIDEO_TEMPLATE_LOCK=1`, `NEWS_TEMPLATE_MEDIA_FIT=contain`, `NEWS_TEMPLATE_MEDIA_BOTTOM_SAFE=580`, and `NEWS_TITLE_SAFE_BOTTOM=580`. Generated/titled videos must scale-to-contain foreground content, center within the media zone, preserve SAR 1:1, output exact 1080x1920, and avoid crop/edge-cutting so the headline/CTA area never covers important subjects. Do not waste empty/black frame: fill any contain padding or spare canvas with a blurred full-bleed copy of the same media behind the foreground.
Use one consistent title font across Instagram cards, Shorts overlays, fallback SVGs, and ffmpeg drawtext overlays: `NEWS_TITLE_FONT_FAMILY="DejaVu Sans"` with `NEWS_TITLE_FONT_BOLD_PATH=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf` and `NEWS_TITLE_FONT_REGULAR_PATH=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`. Instagram/Shorts templates must keep headline font adaptive and bounded so text never covers the hero block: use DejaVu/Arial fallback, smaller default headline sizes, `overflow:hidden`, balanced wrapping, and runtime fit checks in `scripts/genz-news.ts` before screenshot. For ffmpeg fallback overlay, render each title line as a separate `drawtext` textfile (not a multiline textfile) to avoid newline glyph boxes/garbled characters; sanitize emojis, URLs, hashtags, HTML, zero-width characters, and slang before writing the title manifest.
  - Templates should define `--news-title-font` and all headline selectors (`#hookText`, `#titleText`) must use `font-family: var(--news-title-font)`.
- Video title overlay:
  - Instagram/news card template: `/root/nusantara-ai-saas/templates/nusantara_instagram_4x5.html` (`NEWS_IMAGE_CARD_TEMPLATE_PATH`) — 4:5 / 1080x1350, Nusantara-AI News branding, event-scene hero area, bottom headline panel. Instagram PNG output must be the rendered template/card, not the raw generated scene. Keep `NEWS_INSTAGRAM_TEMPLATE_REQUIRED=1`; store raw provider image separately for reference, then screenshot `#slide` as the final Instagram PNG sent to Telegram/Facebook/report. Must expose `#slide`, `#hookText`, `#descText`, `#catPill`, `#slideCounter`, and `#imgZone`. Keep generated media centered and uncropped: default to `object-fit: contain` and `object-position: center center`, but when the user specifically wants a more full-screen flyer, use a tighter frame with smaller inner padding and `object-fit: cover` so the image fills the card edge-to-edge while staying centered. Avoid wasted empty frames: use a full-canvas blurred background (`--hero-bg`) and a larger hero panel so remaining template space feels intentionally filled, not blank.
  - YouTube Shorts overlay template: `/root/nusantara-ai-saas/templates/nusantara_shorts_9x16.html` (`NEWS_VIDEO_OVERLAY_TEMPLATE_PATH`) — 9:16 / 1080x1920, Nusantara-AI News branding, headline card, and subscribe CTA. Must expose `#shorts-canvas`, `#slide` compatibility alias, `#videoZone`, `#imgZone`, `#hookText`, `#descText`, and `#catPill`.
- Keep video/reference media centered and uncropped with `object-fit: contain` and `object-position: center center`; do not revert to `cover` unless user explicitly wants crop.
- When the user asks the Shorts template to *look like the flyer*, keep the flyer’s editorial hierarchy and premium feel, but translate it into a true 9:16 layout: larger hero area, branded top bar, strong bottom headline panel, and blurred full-frame background fill so the frame feels complete rather than empty. Preserve the required IDs above so the pipeline stays compatible.
- If `ffmpeg drawtext` produces garbled glyphs/boxed characters in the Shorts title overlay, switch to a browser-rendered transparent PNG overlay (Playwright/Chromium) and composite it over the video; keep the layout source of truth in the Shorts template and shorten the headline to 1–2 lines.
- See `references/session-2026-05-08-shorts-overlay-browser-fallback.md` for the fallback recipe.
- See `references/session-2026-05-08-chromium-render-and-telegram-caption-verify.md` for the verified Chromium HTML→PNG fallback and Telegram caption verification flow.
  - Legacy template paths may still exist: `/root/nusantara-ai-saas/templates/genz.html` and `/root/nusantara-ai-saas/templates/bot_template.html`, but new automation defaults should use the `nusantara_*` template files unless the user asks otherwise.
  - Command: `npm run gen:viral-news:video-titles -- --video-manifest <path> --template /root/nusantara-ai-saas/templates/nusantara_shorts_9x16.html --aspect 9:16`
- If the hero image feels too low in 4:5, reduce the top empty band and center the crop instead of only shrinking the image.
- When exporting flyer HTML to PNG, render at `1080x1350` for 4:5 and inspect the resulting image with `file` plus visual review; apparent "font problems" are often actually headline/subheadline overlap.
- For natural narration, use a male-presenter Indonesian voice profile and keep the intro concise/news-anchor-like; avoid feeding truncated summaries (`...` / `…`) into TTS because they produce awkward broken phrases.
- For exact-count flyer packs (for example `--count 10`), the default strict score gate may return fewer items than requested. If the user wants the full count, lower `NEWS_MIN_SCORE` / `NEWS_MIN_SINGLE_SCORE` before rendering, then verify the final PNG count and dimensions before reporting success. See `references/session-2026-05-07-10-flyer-threshold-and-render-verification.md`.

- Images to video:
  - `npx tsx scripts/images-to-video.ts --dry-run --prompt "test cinematic realistic action news scene" --output /tmp/test.mp4`

- Secret installation for automation:
  - Use `/root/nusantara-ai-saas/scripts/set-news-automation-secrets.sh` to prompt for new ARK/OpenAI/Telegram bot tokens and write them to `.env` with `chmod 600`.
  - Use `/root/nusantara-ai-saas/scripts/set-meta-page-secrets.sh` to store Facebook Page posting credentials (`META_PAGE_ID`, `META_PAGE_ACCESS_TOKEN`) without printing them. Facebook Page posting uses Meta Graph API `/photos` and is enabled by `NEWS_FACEBOOK_AUTOPOST=1`; it posts the generated 4:5 image plus caption/article link after assets exist.
  - Never copy keys/tokens/passwords from chat transcripts into env files; if keys were pasted into chat, tell the user to rotate/regenerate and enter fresh keys through the prompt-based installer.
  - The installer should print only `set`/`missing` status and `.env` must stay gitignored.
  - For Telegram, store only `TELEGRAM_BOT_TOKEN` in env and keep `TELEGRAM_PUBLIC_CHANNEL_NAME=@nusantaranewsindonesia`; verify the bot is admin in the channel before live sends.
- Direct script entrypoints in this repo often do **not** auto-load `.env`; before running `npm run ...` or `tsx scripts/...` for news generation/publishing, source `.env` (or export the vars in the same shell) so `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, and related secrets are actually visible to the child process.
  - If you plan to shell-source `.env`, quote any values containing spaces first; dotenv may tolerate them, but `source .env` will execute the extra words as commands.
  - User-owned prompt-file runs may need `hermes -z "$(cat /root/.hermes/berita-daily.txt)"` instead of stdin redirection; `hermes chat -z` loads tools and accepts the prompt, while plain `hermes < file` can fail because the CLI expects a terminal on stdin.
  - If a run directory contains the final rendered Instagram PNG but downstream steps still fail on a missing `instagram-4x5-raw/*-raw.png`, inspect the raw provider-image output and manifest before retrying; the presence of the rendered PNG alone is not enough for later pipeline stages.
  - Do not store Gmail/main account passwords for Hostinger/Cloudflare/Byteplus automation; use provider API tokens/OAuth instead.

## Success criteria

Treat the automation as complete only when:
- generation succeeds
- configured Instagram/feed image output is produced (verify `NEWS_INSTAGRAM_ASPECT`, usually `4:5`)
- 9:16 short video output is produced
- article output is produced
- optional Telegram/YouTube delivery succeeds
- final report is written
- public host responds over HTTPS
