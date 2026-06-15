# Session note: OpenAI GPT Images 2.0 for Nusantara-AI image generation

Context: User asked to use `gpt-image-2` for generated images while keeping OpenAI TTS disabled.

## Safe env/config defaults

Use OpenAI only for image generation:

```env
NEWS_IMAGE_PROVIDER=openai
IMAGE_PROVIDER=openai
OPENAI_IMAGE_MODEL=gpt-image-2
NEWS_IMAGE_MODEL=gpt-image-2
NEWS_OPENAI_IMAGE_MODEL=gpt-image-2
NEWS_IMAGE_PROVIDER_ROTATE=openai
IMAGE_PROVIDER_ROTATE=openai
NEWS_NATURAL_NARRATION=0
NEWS_TTS_PROVIDER=disabled
```

Keep `OPENAI_API_KEY` in `.env` or deployment env only. Never copy it into `.env.example`, source files, logs, or final responses.

## Validation command

From `/root/nusantara-ai-saas`:

```bash
set -a; source .env; set +a
NEWS_IMAGE_PROVIDER=openai IMAGE_PROVIDER=openai OPENAI_IMAGE_MODEL=gpt-image-2 \
  npx tsx scripts/prompt-to-images.ts \
  --dry-run \
  --provider openai \
  --openai-model gpt-image-2 \
  --prompt 'cinematic realistic Indonesian public innovation news scene, professional documentary photo, no text, no logo, no watermark' \
  --output /tmp/gpt-image-2-dryrun.png
npm run build:server
```

Expected dry-run payload:
- provider: `openai`
- base URL: `https://api.openai.com/v1`
- endpoint: `/images/generations`
- model: `gpt-image-2`
- output size in this repo may map 4:5 to `1024x1536`

## Provider quirk

A real generation request can fail with HTTP 403:

```text
Your organization must be verified to use the model `gpt-image-2`.
```

This is an OpenAI organization access blocker, not a code bug. Direct the user to verify the OpenAI organization at:

```text
https://platform.openai.com/settings/organization/general
```

Wait up to ~15 minutes after verification before retrying.

## Running the queue after switching to GPT Images

When the user asks to `run automation` after switching image generation to GPT Images 2.0:

1. Stop duplicate queue processes before starting the replacement, otherwise multiple live upload queues can overlap.
2. Start the queue with explicit env overrides as well as `.env`, because wrappers/subprocesses may not inherit the intended provider if relying only on previous shell state:

```bash
set -a; source .env; set +a
export NEWS_IMAGE_PROVIDER=openai IMAGE_PROVIDER=openai OPENAI_IMAGE_MODEL=gpt-image-2 \
  NEWS_IMAGE_PROVIDER_ROTATE=openai IMAGE_PROVIDER_ROTATE=openai \
  NEWS_VIDEO_USE_REFERENCE_IMAGE=0 NEWS_NATURAL_NARRATION=0 NEWS_TTS_PROVIDER=disabled \
  YOUTUBE_QUEUE_SLOTS=24 YOUTUBE_QUEUE_INTERVAL_SECONDS=3600 YOUTUBE_QUEUE_MONITOR_HOURS=24 \
  YOUTUBE_UPLOAD_COUNT=1 NEWS_ARTICLE_AUTOPOST=1 NEWS_MIN_SCORE=90 NEWS_MIN_SINGLE_SCORE=90 NEWS_STRICT_NO_DUPLICATE=1
scripts/run-youtube-hourly-queue.sh --send-telegram
```

3. Verify the active slot actually used OpenAI by reading `data/logs/youtube-hourly-queue-state.json` or `youtube-hourly-queue.log`; the failure text should mention `scripts/prompt-to-images.ts --provider openai` rather than `--provider ark`.
4. Interpret blockers separately:
   - `gpt-image-2` HTTP 403 org-verification = OpenAI image access blocker.
   - `Ark contents/generations/tasks` / `AccountOverdueError` = BytePlus/ARK video blocker.
   - If either blocks media creation, no YouTube/Telegram publish should be claimed.

## Pitfalls

- Do not re-enable OpenAI TTS just because `OPENAI_API_KEY` is present. The user's current policy allows OpenAI for images only.
- Do not claim a real image was generated when the request only passed dry-run or failed due org verification.
- After starting live queue, check the first slot in state/log files before reporting success: `running` only means the scheduler is alive; slot-level failures can still block production output.
- Keep `.env.example` placeholder-only and scan for `sk-`, `ark-`, Telegram bot tokens, OAuth secrets, and signed URLs after edits.
