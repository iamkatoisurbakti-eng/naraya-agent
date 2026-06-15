# Session: video-stage fallback and boolean-flag pitfall

Date: 2026-05-07

## What happened
- `npm run gen:news-pipeline -- --count 1` successfully generated the Instagram 4:5 image and article metadata, but the video stage failed with:
  - `Task gagal: {"code":"InternalServiceError","message":"The service encountered an unexpected internal error."}`
- A direct retry using `scripts/images-to-video.ts` succeeded for the same story when called with the generated 4:5 reference image URL.

## Working fallback
Use the reference image URL from the Instagram manifest and retry the video stage directly:

```bash
ARK_API_KEY="$ARK_API_KEY" \
BYTEDANCE_API_KEY="$BYTEDANCE_API_KEY" \
BYTEPLUS_API_KEY="$BYTEPLUS_API_KEY" \
npx tsx scripts/images-to-video.ts \
  --prompt "<news-specific visual prompt>" \
  --image-url "<reference image url>" \
  --output "<run-dir>/videos/<slug>-9x16.mp4" \
  --ratio 9:16 \
  --duration 15 \
  --scene-count 1 \
  --scene-duration 15 \
  --watermark=false
```

## Important pitfall
- `images-to-video.ts` parses `--generate-audio` as a presence flag. Passing `--generate-audio false` still enables audio because the flag exists.
- If you want to test a silent render, omit the flag entirely or change the script; do not assume `false` disables it.

## Verification
- Use `ffprobe` to confirm the final MP4 is `720x1280` or higher and includes the expected audio stream.
- Check that the scene output exists under `<output>.scenes/scene-01.mp4` when the direct retry succeeds.
