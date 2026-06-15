# Session 2026-05-07 — Visual & Audio Agent setup

## Context

Nusantara-AI pipeline was expanded from ideation/filter/script into a dedicated Visual & Audio Creation Agent for YouTube Shorts production packets.

## Durable decisions

- Agent input is `script_packet` from Script Writing Agent, only after `filter_result.decision=PASS`.
- Output is `visual_audio_packet`, not publish/upload. Publishing remains downstream after Quality Check/Scheduler.
- Target media defaults:
  - YouTube Shorts `9:16`
  - `1080x1920`
  - SEEDANCE/text-to-video prompt-only
  - `NEWS_VIDEO_USE_REFERENCE_IMAGE=0`
  - `generate_audio=true`
  - `NEWS_NATURAL_NARRATION=0`
  - `NEWS_TTS_PROVIDER=disabled`
  - generated-video ambience/action audio only
- Do not run OpenAI `/audio/speech` or `scripts/news-video-natural-narration.ts` unless user explicitly re-enables TTS.
- Do not upload YouTube, send Telegram, publish Facebook/news site, or start the queue from this agent.

## Files created in Nusantara app

- `/root/nusantara-ai-saas/config/visual-audio-agent.json`
- `/root/nusantara-ai-saas/scripts/visual-audio-agent.mjs`
- `/root/nusantara-ai-saas/data/visual-audio/latest.json`
- `/root/nusantara-ai-saas/data/visual-audio/visual-audio-YYYY-MM-DD.jsonl`
- render target: `/root/nusantara-ai-saas/data/visual-audio/renders/*.mp4`

## Cron job

- name: `nusantara-visual-audio-agent-routine`
- job_id: `d91c5d6072ee`
- schedule: `every 3h`
- context_from: Script Writing Agent job `ffdaf3401381`
- skills: `visual-audio-creation-agent`, `filter-agent`, `hermes-agent-orchestration`, `nusantara-news-pipeline-automation`

## Important implementation lesson

Filter positive/public content, not the negative prompt. Negative prompts intentionally include disallowed terms such as `no reporter`, `no running text`, or `no politics`; sending that field through keyword blocking causes false blocks. The runner should filter the positive `video_prompt` and keep `negative_prompt` separate for provider payload.

Also avoid putting negative words inside the positive prompt. Convert script directions like `tanpa reporter/tanpa teks berjalan/tanpa watermark` into positive phrasing such as `cinematic documentary action footage`, `clean static-overlay-safe composition`, and `original generated ambience/action audio`.

## Verification commands

Dry-run packet generation:

```bash
cd /root/nusantara-ai-saas
NEWS_VISUAL_AUDIO_DRY_RUN=1 node scripts/visual-audio-agent.mjs --dry-run --limit=1
```

Optional live render attempt, only if provider readiness is expected:

```bash
cd /root/nusantara-ai-saas
NEWS_VIDEO_USE_REFERENCE_IMAGE=0 \
NEWS_NATURAL_NARRATION=0 \
NEWS_TTS_PROVIDER=disabled \
NEWS_GENERATED_VIDEO_AUDIO_ENABLED=1 \
node scripts/visual-audio-agent.mjs --render --limit=1
```

Validate output status without printing secrets:

```bash
python - <<'PY'
from pathlib import Path
import json
p=Path('/root/nusantara-ai-saas/data/visual-audio/latest.json')
data=json.loads(p.read_text())
item=data['items'][0]
va=item['visual_audio_packet']
print({
  'status': item.get('status'),
  'ready': data.get('ready'),
  'rendered': data.get('rendered'),
  'blocked': data.get('blocked'),
  'filter_decision': va['filter_result']['decision'],
  'use_reference_image': va['use_reference_image'],
  'tts_provider': va['tts_provider'],
  'generate_audio': va['generate_audio'],
  'aspect_ratio': va['settings']['aspect_ratio'],
  'resolution': va['settings']['resolution'],
})
PY
```

## Provider blocker observed

A live render attempt returned ARK/BytePlus HTTP 403 `AccountOverdueError`. Treat that as billing/provider blocker, not agent/pipeline failure. Report as: packet/config ready; live media render blocked until provider balance or fallback provider is fixed. Never print API keys or signed URLs.
