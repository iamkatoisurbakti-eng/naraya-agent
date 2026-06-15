# Session note: fallback reuse after provider failures

Date: 2026-05-08

## What happened
- A live hourly news slot selected a current Technology story from Detik/CNN feeds:
  - `Geotab Rilis Go Focus Plus, Kamera Dasbor AI Buat Cegah Kecelakaan`
- Public article output was saved and verified with HTTP 200 at the exact URL.
- Fresh image generation failed twice:
  - OpenAI prompt enhancer returned `401 invalid_api_key`
  - Ark image generation returned `InvalidEndpointOrModel.NotFound` for `seedream-4.5`
- Fresh video generation was therefore not completed in this slot.
- The run fell back to a verified existing 4:5 PNG + 9:16 MP4 pair from an older run and sent those assets to Telegram.

## Practical lessons
- Treat prompt-enhancer failures as a non-fatal quality layer issue when the raw prompt is still usable.
- Treat `InvalidEndpointOrModel.NotFound` / `AccountOverdueError` / provider 401-403 as generation blockers, not pipeline logic bugs.
- If live generation is blocked and fallback reuse is allowed, only reuse assets that are already present and verified on disk.
- Update the run report explicitly as `fallback-reuse` so the operator does not mistake reused assets for a fresh render.
- Keep Telegram delivery gated on file existence; reuse still requires the image and video files to be real local files.

## Useful verification pattern
1. Save the public article and confirm the public article URL returns HTTP 200.
2. Attempt fresh image/video generation.
3. If provider errors block the run, locate an existing matching PNG/MP4 pair under `data/genz-news/**`.
4. Verify width/height with `ffprobe` before reuse.
5. Send to Telegram only after both reused files exist locally.
