# YouTube Shorts pipeline notes

Session-proven pattern for Nusantara AI SaaS viral/news outputs.

## Shape
- Input: `video-title-manifest.json` produced by the video-title render step.
- Video files are resolved from each manifest entry; upload uses the rendered file path, not manual selection.
- Destination: YouTube Shorts via OAuth 2.0 (client ID, client secret, refresh token).
- Output: a local `youtube-upload-manifest.json` that records per-item upload status/metadata.

## Required env
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`
- optional: `YOUTUBE_PRIVACY_STATUS`, `YOUTUBE_CATEGORY_ID`, `YOUTUBE_MADE_FOR_KIDS`, `YOUTUBE_TAGS`

## Practical pitfalls
- `--dry-run` must short-circuit before any refresh-token or access-token network call.
- In tsx/Node argv handling, a boolean flag may arrive without a value; use a presence check like `process.argv.includes('--dry-run')` (or equivalent) in addition to parsed args.
- Do not log or echo any secret values; keep them redacted in prompts, output, and manifests.
- Upload automation should not assume the manifest file is a source manifest; it may be a derived title/upload manifest with a different schema.

## Shorts formatting
- Shorts support was added by enabling vertical `9:16` output in the video-title renderer (`1080x1920`).
- Keep the pipeline manifest-driven so the same batch can later be reused for Telegram, YouTube, or other channels.

## Verification
- First run: `--dry-run` with a real manifest to confirm selection and output paths.
- Then run one-item live upload before batching the whole set.
- Verify the generated upload manifest and the YouTube response metadata for each item.
