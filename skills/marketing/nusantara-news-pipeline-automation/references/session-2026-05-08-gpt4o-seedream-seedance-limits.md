# GPT-4o + Seedream/Seedance limit mapping

Session note for the Nusantara-AI News automation stack.

## Observed production mapping
- Flyers:
  - `NEWS_IMAGE_PROVIDER=ark`
  - `NEWS_IMAGE_MODEL=seedream-4.5`
  - `NEWS_FLYER_PROMPT_PROVIDER=openai`
  - `NEWS_FLYER_PROMPT_MODEL=gpt-4o`
- Shorts:
  - `NEWS_VIDEO_MODEL=seedance-1.5-pro`
  - `NEWS_VIDEO_PROMPT_PROVIDER=openai`
  - `NEWS_VIDEO_PROMPT_MODEL=gpt-4o`

## How it behaves
- GPT-4o is used as a *prompt rewrite* stage.
- GPT-4o does **not** replace the image/video provider; it just improves the prompt before the provider runs.
- Keep the image/video provider selection explicit in env so the pipeline remains predictable.

## Useful dry-runs
- Flyer prompt payload preview:
  - `npx tsx scripts/prompt-to-images.ts --dry-run --provider ark --prompt '...'`
- Shorts scene preview:
  - `npx tsx scripts/images-to-video.ts --dry-run --prompt '...'`
- Combined automation preview:
  - `npx tsx scripts/news-pipeline.ts --dry-run --count 5`

## Notes from this session
- `images-to-video.ts` defaults to 2 scenes for a 30s short using 15s per scene.
- The pipeline can be run in count-based batches for flyer+short automation; verify the resulting `steps` and manifest paths before claiming success.
- For the live pipeline, keep `NEWS_VIDEO_USE_REFERENCE_IMAGE=0` unless the user explicitly asks to reuse the Instagram image as a reference for video generation.
