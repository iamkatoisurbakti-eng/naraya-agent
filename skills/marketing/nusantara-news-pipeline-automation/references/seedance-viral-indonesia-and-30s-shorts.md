# SEEDANCE Indonesia viral-news focus and 30-second Shorts duration policy

Session context: the Nusantara-AI News agent chain was tightened so SEEDANCE focuses on viral Indonesia news data and all YouTube Shorts are capped at 30 seconds.

## SEEDANCE ideation focus

Stable config:
- `/root/nusantara-ai-saas/config/content-ideation.json`
- `.env` keys only; never print values.

Core env keys:
```env
NEWS_IDEATION_PROVIDER=seedance
NEWS_IDEATION_DATA_FOCUS=indonesia_viral_news
NEWS_IDEATION_MARKET=Indonesia
NEWS_IDEATION_COUNTRY=ID
NEWS_IDEATION_LANGUAGE=id
NEWS_IDEATION_TREND_SIGNALS=freshness_today,national_relevance,search_social_interest,shareability,shorts_hook_strength,visual_event_scene_potential,trusted_source_pickup_count
NEWS_IDEATION_MIN_TREND_SIGNAL_SCORE=90
NEWS_IDEATION_MIN_VIRALITY_SCORE=90
NEWS_IDEATION_MIN_SOURCE_TRUST_SCORE=85
NEWS_IDEATION_SENTIMENT_ALLOWLIST=positive,neutral
NEWS_IDEATION_TRUSTED_SOURCE_POLICY=allowlist_only
```

Trusted-source allowlist used in this setup:
- ANTARA News, Kompas, Detik, CNN Indonesia, CNBC Indonesia, Tempo, Katadata, Bisnis Indonesia, Liputan6, Republika, Media Indonesia.

SEEDANCE/ARK status should be reported as booleans only:
- `SEEDANCE_API_KEY` set/missing
- `ARK_API_KEY` set/missing fallback

## 30-second Shorts policy

User preference: all Nusantara-AI Shorts videos must be <=30 seconds. Target 20-30s, implemented as 2 scenes x 15s.

Stable env/config:
```env
NEWS_PIPELINE_VIDEO_DURATION=30
NEWS_VIDEO_TARGET_DURATION_SECONDS=30
NEWS_VIDEO_MAX_DURATION_SECONDS=30
NEWS_VIDEO_SCENE_COUNT=2
NEWS_VIDEO_SCENE_DURATION_SECONDS=15
NEWS_VISUAL_AUDIO_DURATION_SECONDS=30
NEWS_VISUAL_AUDIO_SCENE_COUNT=2
NEWS_VISUAL_AUDIO_SCENE_DURATION_SECONDS=15
NEWS_QC_IDEAL_MIN_SECONDS=20
NEWS_QC_IDEAL_MAX_SECONDS=30
NEWS_QC_ABSOLUTE_MAX_SECONDS=30
```

Files touched in the setup:
- `/root/nusantara-ai-saas/config/visual-audio-agent.json`
- `/root/nusantara-ai-saas/config/quality-check-agent.json`
- `/root/nusantara-ai-saas/scripts/news-pipeline.ts`
- `/root/nusantara-ai-saas/scripts/images-to-video.ts`
- `/root/nusantara-ai-saas/scripts/visual-audio-agent.mjs`
- `/root/nusantara-ai-saas/scripts/quality-check-agent.mjs`
- `/root/nusantara-ai-saas/docker-compose.yml`

Important implementation detail: `images-to-video.ts` had a hardcoded `DEFAULT_SCENE_COUNT = 4`; update it to read `NEWS_VIDEO_SCENE_COUNT || 2`, otherwise a 30s dry-run can still emit 4 x 15s scenes.

## Validation commands

Run from `/root/nusantara-ai-saas`:

```bash
NEWS_VISUAL_AUDIO_DRY_RUN=1 node scripts/visual-audio-agent.mjs --dry-run --limit=1
npx tsx scripts/images-to-video.ts --dry-run --prompt 'test cinematic realistic Indonesian news scene, no text' --output /tmp/test-30s.mp4
node scripts/quality-check-agent.mjs --limit=5
npm run build:server
```

Expected dry-run assertions:
- visual/audio packet: `duration_seconds=30`, `scene_count=2`, scene durations `[15,15]`, total `30`.
- images-to-video dry-run: `duration=30`, `sceneDuration=15`, `sceneTotal=2`, `ratio=9:16`, `watermark=false`, `generateAudio=true`.
- QC duration gate: ideal max 30 and absolute max 30. A rendered video >30s must not publish.

## Pitfalls

1. Do not only change config; check scripts for hardcoded 60s or 4-scene defaults.
2. When updating duration, patch Script Writing, Visual & Audio, Quality Check, Scheduler/cron prompts, `.env`, `.env.example`, and Docker env passthrough together.
3. If the provider is blocked by `AccountOverdueError`, validation can still confirm dry-run payloads but real render/QC will remain `SKIP` until a valid video exists.
4. Do not lower QC score or bypass QC because the video is shorter; `PUBLISH` still requires score >=90, 9:16 1080x1920, generated-video audio, no watermark, no running text, and Filter Agent PASS.
