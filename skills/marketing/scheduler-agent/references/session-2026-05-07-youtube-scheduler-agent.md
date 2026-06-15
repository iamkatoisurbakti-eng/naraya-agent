# Session 2026-05-07 — Scheduler Agent YouTube API Gate

## Context

User requested an Agen Penjadwal that uploads and schedules automatically to YouTube with a YouTube Scheduler API/OAuth flow. This extends the Nusantara-AI News agent chain after Quality Check Agent.

## Files Created in `/root/nusantara-ai-saas`

- `config/scheduler-agent.json`
- `scripts/scheduler-agent.mjs`
- output directory: `data/scheduler/`
- latest report: `data/scheduler/latest.json`
- JSONL audit log: `data/scheduler/scheduler-YYYY-MM-DD.jsonl`

Cron job created:

- Job ID: `741a6fd84372`
- Name: `nusantara-scheduler-agent-youtube-routine`
- Schedule: every 3h
- `context_from`: Quality Check job `925f3108ab92`

## Required Gate Order

Scheduler must never upload just because YouTube OAuth exists. It must gate in this order:

1. `quality_check.decision == PUBLISH`
2. `quality_check.total_score >= 90`
3. `filter_result.decision == PASS`
4. final video exists and `ffprobe` can read it
5. video is vertical 9:16 and at least `1080x1920`
6. audio stream exists when audio is required
7. YouTube OAuth env is present (`YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`)
8. no active duplicate YouTube queue process exists

If any gate fails, write `scheduler_decision` as `SKIP_SLOT` or `HOLD`; do not call upload.

## Safe Env/Defaults

Non-secret defaults set in `.env`/`.env.example`:

- `NEWS_SCHEDULER_AGENT_ENABLED=1`
- `NEWS_SCHEDULER_CONFIG_PATH=/root/nusantara-ai-saas/config/scheduler-agent.json`
- `NEWS_SCHEDULER_MODE=hourly_queue`
- `NEWS_SCHEDULER_TIMEZONE=Asia/Jakarta`
- `NEWS_SCHEDULER_MIN_PUBLISH_SCORE=90`
- `YOUTUBE_QUEUE_SLOTS=24`
- `YOUTUBE_QUEUE_INTERVAL_SECONDS=3600`
- `YOUTUBE_QUEUE_MONITOR_HOURS=24`
- `YOUTUBE_UPLOAD_COUNT=1`
- `YOUTUBE_PRIVACY_STATUS=public`
- `YOUTUBE_MADE_FOR_KIDS=0`
- `YOUTUBE_TARGET_COUNTRY=ID`
- `YOUTUBE_DEFAULT_LANGUAGE=id`
- `YOUTUBE_LOCATION_DESCRIPTION=Indonesia`
- `YOUTUBE_CATEGORY_ID=25`
- `YOUTUBE_GROWTH_MODE=1`
- `NEWS_YOUTUBE_GROWTH_MODE=1`

Never print actual OAuth token/secret values.

## Commands

Dry-run scheduler:

```bash
cd /root/nusantara-ai-saas
NEWS_SCHEDULER_DRY_RUN=1 node scripts/scheduler-agent.mjs --dry-run --limit=5
```

Inspect report:

```bash
cat data/scheduler/latest.json
```

Check duplicate queue processes without printing secrets:

```bash
ps -eo pid,cmd | grep -E 'news-youtube-hourly-queue|run-youtube-hourly-queue|gen:news-youtube-queue' | grep -v grep || true
```

Validate server build:

```bash
npm run build:server
```

## Observed Dry-Run Result

Latest dry-run saw:

- `youtube_oauth_ready=true`
- `filter_ok=true`
- `quality_decision_ok=false`
- `quality_score_ok=false`
- `video_ready=false`
- `audio_ok=false`
- `duplicate_queue_ok=false`
- decision: `SKIP_SLOT`
- reason: `skipped_quality_gate`

This was correct: the latest QC item was `SKIP` score 45 because the video was not rendered. A YouTube queue was also already running, so starting another would risk double upload.

## Provider/Billing Pitfall

If render failed earlier with ARK/BytePlus/SEEDANCE `AccountOverdueError`, scheduler should not diagnose YouTube as broken. Treat it as upstream media-generation blocker; scheduler should hold/skip until a valid rendered video and QC `PUBLISH` report exist.

## Key Lesson

A scheduler is not an uploader shortcut. It is a final gatekeeper. In this pipeline, a ready OAuth credential is necessary but never sufficient for upload.
