# Rotating Ark/OpenAI image providers

Use this note when the pipeline needs to alternate image generation providers for Nusantara-AI News.

## Behavior
- Rotation order: `ark,openai`.
- Enabled by setting the image provider to `rotate`.
- If only one provider key is available, fall back to that provider automatically.
- The manifest should record which provider was used per item.

## Env defaults used in production
- `NEWS_IMAGE_PROVIDER=rotate`
- `NEWS_IMAGE_PROVIDER_ROTATE=ark,openai`

## Verification
- Dry-run the pipeline and confirm manifest items alternate providers.
- Check container env only for presence/absence of keys; never print secret values.

## Pitfalls
- A code default alone is not enough if compose overrides do not enable rotate.
- Dry-run may look correct while production still uses stale container env unless the service is redeployed.
- Keep the fallback logic provider-aware so missing OpenAI does not break Ark and vice versa.
