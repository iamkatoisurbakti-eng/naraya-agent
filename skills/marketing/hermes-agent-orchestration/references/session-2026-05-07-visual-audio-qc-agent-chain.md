# 2026-05-07 — Visual/Audio + QC Agent Chain for Nusantara-AI News

## Context

User requested the agent chain to progress beyond ideation and scripting:

- Visual & Audio Creation Agent: produce YouTube Shorts video with relevant clips/images/audio.
- Quality Check Agent: ensure short duration, high quality, and forbidden-content-free output.

This was implemented as class-level Hermes skills plus local repo configs/runners and recurring cron jobs. The chain remains safe: it prepares/render-checks assets, but does not upload YouTube, send Telegram, publish, run the hourly queue, or expose secrets.

## Artifacts Created

### Visual & Audio Creation Agent

Skill:
- `/root/.hermes/skills/marketing/visual-audio-creation-agent/SKILL.md`

Repo files:
- `/root/nusantara-ai-saas/config/visual-audio-agent.json`
- `/root/nusantara-ai-saas/scripts/visual-audio-agent.mjs`
- `/root/nusantara-ai-saas/data/visual-audio/latest.json`
- `/root/nusantara-ai-saas/data/visual-audio/visual-audio-YYYY-MM-DD.jsonl`
- `/root/nusantara-ai-saas/data/visual-audio/renders/*.mp4` if render succeeds

Cron:
- Job ID: `d91c5d6072ee`
- Name: `nusantara-visual-audio-agent-routine`
- Schedule: every 3h
- Context source: Script Writing Agent job `ffdaf3401381`
- Skills: `visual-audio-creation-agent`, `filter-agent`, `hermes-agent-orchestration`, `nusantara-news-pipeline-automation`

### Quality Check Agent

Skill patched:
- `/root/.hermes/skills/marketing/quality-check-agent/SKILL.md`

Repo files:
- `/root/nusantara-ai-saas/config/quality-check-agent.json`
- `/root/nusantara-ai-saas/scripts/quality-check-agent.mjs`
- `/root/nusantara-ai-saas/data/quality-check/latest.json`
- `/root/nusantara-ai-saas/data/quality-check/quality-check-YYYY-MM-DD.jsonl`

Cron:
- Job ID: `925f3108ab92`
- Name: `nusantara-quality-check-agent-routine`
- Schedule: every 3h
- Context source: Visual & Audio Agent job `d91c5d6072ee`
- Skills: `quality-check-agent`, `filter-agent`, `hermes-agent-orchestration`

## Important Runner Behavior

### `scripts/visual-audio-agent.mjs`

Inputs:
- Reads `/root/nusantara-ai-saas/data/content-scripts/latest.json`.
- Processes only `SCRIPT_READY`/`script_packet` items.
- Runs `scripts/content-filter.mjs` before making visual/audio packets.

Outputs:
- Writes `visual_audio_packet` with `provider=seedance`, `use_reference_image=false`, `generate_audio=true`, `tts_provider=disabled`, settings `9:16`, `1080x1920`, `scene_count=4`, `scene_duration_seconds=15`.

Prompt handling lesson:
- Run Filter Agent on the positive production prompt only.
- `negative_prompt` intentionally contains forbidden words (e.g. no reporter/no politics/no gore) and should not trigger blocking by itself.
- Keep positive prompt free of forbidden terms like `running text`, `watermark`, `reporter`, `anchor`, `newsroom`, `voice-over`, `dialogue`, and `popular music`; put exclusions in negative prompt.

Render behavior:
- `--dry-run` writes READY packet only.
- `--render` calls `npx tsx scripts/images-to-video.ts` with `NEWS_VIDEO_USE_REFERENCE_IMAGE=0`, `NEWS_NATURAL_NARRATION=0`, `NEWS_TTS_PROVIDER=disabled`, `NEWS_GENERATED_VIDEO_AUDIO_ENABLED=1`.
- Do not run OpenAI TTS or `scripts/news-video-natural-narration.ts`.

Known blocker from this session:
- Render returned ARK/BytePlus HTTP 403 `AccountOverdueError`.
- Treat that as provider/billing blocker, not a pipeline/agent bug. QC must not publish in this state.

### `scripts/quality-check-agent.mjs`

Inputs:
- Reads `/root/nusantara-ai-saas/data/visual-audio/latest.json`.

Checks:
- Runs Filter Agent on public text and positive prompt.
- Uses `ffprobe` for video metadata when the video exists.
- Scores duration/format, audio quality, trend fit, and visual/brand compliance.
- Requires `total_score >= 90`, `filter_result.decision=PASS`, valid video metadata, and no critical issues before PUBLISH.

Gate rules:
- Missing video or unreadable metadata => critical issue => SKIP.
- Missing audio when audio required => critical issue => SKIP.
- Filter BLOCK => SKIP.
- Filter REVIEW or score <90 => RETRY/SKIP depending severity.

Session validation result:
- Visual/audio dry run: READY, filter PASS, `use_reference_image=false`, `tts_provider=disabled`, `generate_audio=true`, `aspect_ratio=9:16`, `resolution=1080x1920`.
- Actual render: failed due provider `AccountOverdueError`.
- QC result: score 45, decision SKIP, filter PASS, critical issue `Video belum tersedia/metadata tidak valid.`

## Env Defaults Added

Visual/audio:
- `NEWS_VISUAL_AUDIO_AGENT_ENABLED=1`
- `NEWS_VISUAL_AUDIO_CONFIG_PATH=/root/nusantara-ai-saas/config/visual-audio-agent.json`
- `NEWS_VISUAL_AUDIO_LIMIT=1`
- `NEWS_VIDEO_PROVIDER=seedance`
- `NEWS_AUDIO_PROVIDER=seedance`
- `NEWS_VIDEO_USE_REFERENCE_IMAGE=0`
- `NEWS_NATURAL_NARRATION=0`
- `NEWS_TTS_PROVIDER=disabled`
- `NEWS_GENERATED_VIDEO_AUDIO_ENABLED=1`
- `NEWS_VIDEO_WATERMARK=0`
- `NEWS_NO_RUNNING_TEXT=1`
- `NEWS_VIDEO_NO_RUNNING_TEXT=1`

Quality check:
- `NEWS_QC_ENABLED=1`
- `NEWS_QC_CONFIG_PATH=/root/nusantara-ai-saas/config/quality-check-agent.json`
- `NEWS_QC_MIN_PUBLISH_SCORE=90`
- `NEWS_QC_REQUIRE_FILTER_PASS=1`
- `NEWS_QC_REQUIRE_AUDIO=1`
- `NEWS_QC_MIN_DURATION_SECONDS=15`
- `NEWS_QC_IDEAL_MIN_DURATION_SECONDS=30`
- `NEWS_QC_MAX_DURATION_SECONDS=60`
- `NEWS_QC_MIN_WIDTH=1080`
- `NEWS_QC_MIN_HEIGHT=1920`

Never print env values for keys/tokens. Only report set/missing and `.env` mode.

## Verification Commands

Visual/audio dry run:

```bash
cd /root/nusantara-ai-saas
NEWS_VISUAL_AUDIO_DRY_RUN=1 node scripts/visual-audio-agent.mjs --dry-run --limit=1
```

Optional render (only when provider is funded/ready):

```bash
cd /root/nusantara-ai-saas
NEWS_VIDEO_USE_REFERENCE_IMAGE=0 \
NEWS_NATURAL_NARRATION=0 \
NEWS_TTS_PROVIDER=disabled \
NEWS_GENERATED_VIDEO_AUDIO_ENABLED=1 \
node scripts/visual-audio-agent.mjs --render --limit=1
```

QC:

```bash
cd /root/nusantara-ai-saas
node scripts/quality-check-agent.mjs --limit=5
```

Inspect outputs:

```bash
cat /root/nusantara-ai-saas/data/visual-audio/latest.json
cat /root/nusantara-ai-saas/data/quality-check/latest.json
```

## Pitfalls

1. Do not filter the negative prompt as user-facing content; it can include forbidden terms because it is an exclusion list.
2. Do not claim a video was produced unless the target MP4 exists and `ffprobe` can read it.
3. Do not bypass QC because the visual/audio packet is READY; READY means prompt/payload ready, not rendered media valid.
4. Do not publish when provider billing blocks render. QC should SKIP with missing video metadata.
5. Do not enable OpenAI TTS to satisfy the “audio” requirement; current user preference is generated-video/SEEDANCE ambience only.
