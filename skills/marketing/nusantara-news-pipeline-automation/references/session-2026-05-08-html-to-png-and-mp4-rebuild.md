# Session note: HTML → PNG export and MP4 rebuild

## What worked
- Local HTML files were exported to PNG using Playwright/Chromium with `page.setContent(...)`.
- For interactive Shorts HTML, calling `window.startVideo()` before the screenshot captured the first scene correctly.
- The reusable helper now lives at `scripts/render-html-to-png.mjs`.

## Verification
- `file flyer-2026-05-08.png` returned `1080 x 1350`.
- `file video-2026-05-08.png` returned `1080 x 1920`.
- `ffprobe` confirmed the rebuilt MP4 at `1080x1920` with `30.04s` duration.

## Pitfall and fallback
- The initial MP4 had `moov atom not found`, so it was rebuilt from `video-frames.txt` using ffmpeg concat:
  - `ffmpeg -y -f concat -safe 0 -i video-frames.txt -fps_mode vfr -pix_fmt yuv420p -movflags +faststart output.mp4`
- If a future MP4 render fails to probe, check whether the frame list exists and rebuild from frames before assuming the video pipeline is broken.

## Practical notes
- Use `--selector #slide` for template-based screenshots when the template exposes a stable root node.
- Use `--start-video` for preview pages that need JS to reveal the first scene before capture.
- Keep the PNG export step separate from video muxing; image export should not wait on a valid MP4 file.
