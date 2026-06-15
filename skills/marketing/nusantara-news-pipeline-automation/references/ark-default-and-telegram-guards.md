# Ark default + Telegram guards

Session learning:
- Default provider for `prompt-to-images.ts` and `news-pipeline.ts` should be `ark` unless the user explicitly enables rotation.
- Production compose should set `NEWS_IMAGE_PROVIDER=ark` by default; `NEWS_IMAGE_PROVIDER_ROTATE` can still exist as an opt-in override.
- Telegram delivery must be guarded by file existence checks:
  - do not send an image item unless the rendered image file exists
  - do not send a video item unless both the final image/reference and final video file exist
- This prevents partial sends when a render step silently fails or is skipped.

Practical verification:
- Dry-run pipeline should still complete when no external render/upload happens.
- Runtime manifests should show `provider: ark` for image generation when defaults are used.
- Telegram send loops should log a skip reason instead of throwing when assets are missing.
