# Session note: Ark/OpenAI rotation and media gates

- When image provider rotation is enabled, alternate Ark and OpenAI across generated images instead of hard-locking one provider.
- For production verification, confirm the container env actually contains:
  - `NEWS_IMAGE_PROVIDER=rotate`
  - `NEWS_IMAGE_PROVIDER_ROTATE=ark,openai`
- Single-item runs must enforce the 95+ score gate before any image/video rendering.
- Telegram sending must skip any item with missing required media:
  - image send requires the rendered image file
  - video send requires both the rendered image reference and final video file
- Use clear skip reasons in logs: `missing image`, `missing video`, or `missing both`.
- Rotation verification tip: check the generated manifest; the `provider` field should alternate `ark`, `openai`, `ark`, `openai` across items when both keys are available.
