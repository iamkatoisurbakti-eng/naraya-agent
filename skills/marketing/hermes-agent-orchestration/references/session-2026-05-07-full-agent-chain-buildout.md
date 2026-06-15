# Session 2026-05-07 — Nusantara-AI Agent Chain Buildout

## Scope

This session extended the class-level Nusantara-AI News agent workflow rather than adding unrelated one-off skills. User asked for a sequence of agents:

1. Content Ideation Agent with SEEDANCE analyzer for trusted positive/neutral Indonesian viral news.
2. Filter Agent for forbidden categories.
3. Script Writing Agent for short, light, interesting scripts from filtered results.
4. Visual & Audio Creation Agent for YouTube Shorts video/audio packets.
5. Quality Check Agent for duration, quality, and forbidden-content gate.
6. Scheduler Agent for YouTube Scheduler API/OAuth gate.

## Agent Chain

Canonical order:

```text
Content Ideation Agent
  -> Filter Agent
  -> Script Writing Agent
  -> Filter Agent
  -> Visual & Audio Creation Agent
  -> Filter Agent
  -> Quality Check Agent
  -> Scheduler Agent
  -> Publishing/Distribution Agent
```

Every handoff must carry `content_id` and a structured packet. Do not skip gates just to keep a queue full.

## Stable Repo Artifacts

Config/runner paths established in `/root/nusantara-ai-saas`:

- `config/content-ideation.json`
- `config/content-filter.json`
- `config/visual-audio-agent.json`
- `config/quality-check-agent.json`
- `config/scheduler-agent.json`
- `scripts/content-filter.mjs`
- `scripts/visual-audio-agent.mjs`
- `scripts/quality-check-agent.mjs`
- `scripts/scheduler-agent.mjs`

Output directories:

- `data/content-ideas/`
- `data/content-scripts/`
- `data/visual-audio/`
- `data/quality-check/`
- `data/scheduler/`

Cron jobs:

- Content Ideation Agent: `88cf553230f7`
- Script Writing Agent: `ffdaf3401381`
- Visual & Audio Creation Agent: `d91c5d6072ee`
- Quality Check Agent: `925f3108ab92`
- Scheduler Agent: `741a6fd84372`

## Important Cross-Agent Rules

- Filter Agent must run before scripting, before visual/audio rendering, and before publishing.
- Filter only the positive/public prompt text; keep negative prompts separate because they intentionally list excluded concepts.
- Script style requested: `ringan-menarik-baku` — light and engaging, but still Bahasa Indonesia baku/KBBI style.
- Visual/video default remains prompt-only: `NEWS_VIDEO_USE_REFERENCE_IMAGE=0`.
- Audio default remains generated-video ambience/action audio only; no OpenAI TTS, no `/audio/speech`.
- QC gate must require score >=90 and `decision=PUBLISH` before Scheduler can upload/schedule.
- Scheduler must check duplicate YouTube queues before upload.
- Provider `AccountOverdueError` is an upstream media generation/billing blocker, not a scheduler/YouTube bug.

## Verification Commands

Filter check:

```bash
node scripts/content-filter.mjs --text='Kabar positif tentang inovasi teknologi pendidikan Indonesia'
```

Visual/audio dry-run:

```bash
NEWS_VISUAL_AUDIO_DRY_RUN=1 node scripts/visual-audio-agent.mjs --dry-run --limit=1
```

QC run:

```bash
node scripts/quality-check-agent.mjs --limit=5
```

Scheduler dry-run:

```bash
NEWS_SCHEDULER_DRY_RUN=1 node scripts/scheduler-agent.mjs --dry-run --limit=5
```

Build verification:

```bash
npm run build:server
```

## Lessons for Future Sessions

1. When the user asks for an agent, implement the class-level agent and connect it to the pipeline; do not treat it as a mere prompt template.
2. Keep outputs auditable in `data/<stage>/latest.json` and daily JSONL files.
3. Use dry-run first, then live render/upload only when gates pass.
4. Never print credential values; report only `set`/`missing`.
5. If QC fails due to missing rendered video, scheduler must skip/hold even if YouTube OAuth is ready.
