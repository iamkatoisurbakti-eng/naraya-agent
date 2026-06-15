# Session Note: OpenAI flyer prompt enhancer fallback

Date: 2026-05-08

Observed issue:
- `enhanceFlyerPrompt()` could fail with OpenAI HTTP 401 when `NEWS_FLYER_PROMPT_PROVIDER=openai` and `NEWS_FLYER_PROMPT_MODEL` were set, causing the pipeline to stop before image/video generation.

Verified fix pattern:
- Treat enhancer failure as non-fatal.
- If the enhancer returns non-OK or throws, continue with the original raw prompt.
- Log a warning only; do not claim image generation failed because the enhancer failed.

Operational implication:
- Prompt enhancement is an optional quality layer, not a hard dependency.
- Live runs should still proceed to image/video generation when the enhancer is unavailable or misconfigured.

Related code path:
- `scripts/news-pipeline.ts` → `enhanceFlyerPrompt()`
