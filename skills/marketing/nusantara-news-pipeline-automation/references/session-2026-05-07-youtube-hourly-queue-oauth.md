# Session 2026-05-07: YouTube hourly queue + OAuth credential handling

## What changed

Nusantara AI SaaS now has an hourly YouTube queue path for news automation:

- `scripts/news-youtube-hourly-queue.ts`
- `scripts/run-youtube-hourly-queue.sh`
- npm script: `gen:news-youtube-queue`

Default queue behavior:

- `YOUTUBE_QUEUE_SLOTS=12`
- `YOUTUBE_QUEUE_INTERVAL_SECONDS=3600`
- `YOUTUBE_QUEUE_MONITOR_HOURS=24`
- `NEWS_MIN_SCORE=90`
- `NEWS_MIN_SINGLE_SCORE=90`
- `NEWS_INSTAGRAM_ASPECT=4:5`
- `NEWS_NATURAL_NARRATION=1`

Run command:

```bash
cd /root/nusantara-ai-saas
scripts/run-youtube-hourly-queue.sh
```

Dry-run verification command:

```bash
NEWS_MIN_SCORE=90 NEWS_MIN_SINGLE_SCORE=90 NEWS_INSTAGRAM_ASPECT=4:5 \
  npm run gen:news-youtube-queue -- --dry-run --skip-video --slots 1 --interval-seconds 1 --monitor-hours 0.001
```

Logs/state:

- `data/logs/youtube-hourly-queue.log`
- `data/logs/youtube-hourly-queue-state.json`

## Scoring/backtest gate

`scripts/genz-news.ts` was tightened so multi-item runs also filter by score, not just single-item runs:

- `NEWS_MIN_SCORE` controls general threshold.
- `NEWS_MIN_SINGLE_SCORE` controls one-item mode, defaulting to `NEWS_MIN_SCORE`.
- Candidates below threshold are rejected before image/video/upload stages.
- Manifest now records `minScore`, `selectionPolicy`, `votes`, `judgeScores`, `historyMatch`, and `kbbiQuality` when available.

This satisfies user requests like “scoring di bawah 90 jangan digunakan.”

## Instagram aspect

`scripts/news-pipeline.ts` now supports:

- `NEWS_INSTAGRAM_ASPECT=4:5`

The image output directory and manifest use the aspect, e.g. `instagram-4x5` and `instagram-4x5-manifest.json`. Keep UI/text convention numeric-only (`4:5`, `9:16`).

## YouTube OAuth credential status

A valid Google Desktop OAuth client JSON was found at:

```text
/root/.hermes/client_secret_1061338379955-39a7j4c6cpsu3m652be1pnkpi9mrqe1e.apps.googleusercontent.com.json
```

Safe validation details only:

- type/mode: `installed`
- project_id: `teak-clone-494608-s1`
- client_id present
- client_secret present
- auth_uri/token_uri present
- redirect_uris includes `http://localhost`
- sha256: `aa10072b0bd8defe90018251f9f81a68f0f890b8b621983f54371fd7e89d50ff`

Do not print client_secret or full tokens. The repo `.env` still lacked:

- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

## Next OAuth step pattern

To finish YouTube upload setup:

1. Extract `client_id` and `client_secret` from the JSON into `.env` without echoing values.
2. Generate an OAuth authorization URL for YouTube Data API upload scope.
3. User opens the URL, logs into Gmail/YouTube channel account, approves consent.
4. User returns the redirected URL/code.
5. Exchange code for refresh token.
6. Store `YOUTUBE_REFRESH_TOKEN` in `.env` without printing it.
7. Run a dry-run, then live queue.

Important: YouTube upload needs OAuth 2.0, not a simple API key. Do not use Gmail password. If any secret was pasted in chat, treat it as compromised and ask the user to rotate/regenerate before storing via prompt/env.

## Verification already done

- `package.json` parse OK.
- `npm run build:server` OK after queue changes.
- Queue dry-run one-slot OK.
- State file reflected `minScore=90` and `instagramAspect=4:5`.
