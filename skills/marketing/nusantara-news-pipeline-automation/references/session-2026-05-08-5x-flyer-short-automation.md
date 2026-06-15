# Session note: 5 flyer + 5 short automation

Date: 2026-05-08
Scope: Nusantara-AI News batch automation run for 5 flyers + 5 shorts per run.

## What worked
- `npx tsx scripts/news-pipeline.ts --dry-run --count 5` completed successfully for planning/manifest preview.
- The run folder produced 5 Instagram flyer PNGs plus `manifest.json` / `instagram-4x5-manifest.json`.
- Caption format in manifests included a complete publish-ready block and exactly 4 hashtags.

## Model / provider mapping used during the session
- Flyer image model: `seedream-4-0-250828`
- Flyer prompt enhancer: `NEWS_FLYER_PROMPT_PROVIDER=openai`, `NEWS_FLYER_PROMPT_MODEL=gpt-4o`
- Video prompt provider/model: `NEWS_VIDEO_PROMPT_PROVIDER=openai`, `NEWS_VIDEO_PROMPT_MODEL=gpt-4o`
- Shorts video model attempted successfully only when set to `dreamina-seedance-2-0-260128`
- `NEWS_VIDEO_USE_REFERENCE_IMAGE=0` for prompt-only shorts generation

## Failure modes observed
1. `InvalidEndpointOrModel.NotFound`
   - caused by an unavailable/non-accessible video model (`seedance-1.5-pro`)
   - fix: switch to a supported model and verify access before claiming completion
2. `AccountOverdueError`
   - returned by Ark/BytePlus video generation when the account had overdue balance
   - fix: resolve billing/provider state or use a fallback media route

## Verification checklist for this batch mode
- Confirm exactly 5 flyer PNGs exist in the run directory
- Confirm each caption is complete and has exactly 4 hashtags
- Confirm the batch count in the pipeline manifest/report is 5
- Confirm Shorts video generation reaches `video-manifest.json` and `pipeline-report.json` before calling the run complete
- If video generation fails, report the failure as a blocked batch rather than a successful 5x5 delivery
