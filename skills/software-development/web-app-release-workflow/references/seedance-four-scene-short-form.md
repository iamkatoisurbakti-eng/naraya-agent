# Seedance four-scene short-form pattern

Use this when the video model only supports ~15 seconds per generation but the product needs a longer Shorts-style output.

Pattern
- Treat each scene as a distinct prompt.
- Default to 4 scenes for a full short-form video:
  1. hook / opening headline
  2. development / context
  3. deeper detail / impact
  4. closing / recap / CTA
- Keep each scene at 15 seconds.
- For Shorts delivery, target 9:16 and enforce a minimum 720x1280 final raster when the provider output is smaller.
- Concatenate the rendered clips with ffmpeg into one final video.

Implementation notes
- In the generator script, expose:
  - `--scene-count 4`
  - `--scene-duration 15`
  - default total `--duration 60`
- Build prompt text per scene so each clip has a unique beat instead of reusing the same prompt.
- If the final scene duration would become a short remainder, clamp each scene to a full 15 seconds for consistency when the model is capped at 15s anyway.
- Prefer a temp folder per output, then use ffmpeg concat demuxer to merge clips.

Verification
- Dry-run should show 4 generated scene payloads.
- Confirm each payload has `duration: 15`.
- Confirm the final merged output path exists after a real run.

Useful command
- `npx tsx scripts/images-to-video.ts --dry-run --prompt "..." --image-url https://example.com/test.jpg --output /tmp/news-short.mp4`
