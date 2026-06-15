# Chromium HTML→PNG Fallback and Telegram Caption Verification

Session note: 2026-05-08

## What worked

When Playwright/Chromium screenshotting a local `file:///...html` page is needed and the default browser path is unstable, the snap Chromium binary can still succeed in headless mode:

```bash
/snap/bin/chromium \
  --headless \
  --no-sandbox \
  --disable-gpu \
  --screenshot=/path/to/output.png \
  --window-size=1080,1350 \
  file:///path/to/page.html
```

Observed behavior:
- DBus/AppArmor accessibility warnings may print.
- Those warnings are noisy but not necessarily fatal.
- Success is determined by the screenshot file being written and readable.

## Video HTML fallback for frame capture

For interactive 9:16 HTML pages that start with an overlay or hidden first scene:
- hide the overlay before screenshot, or
- call `window.startVideo()` if the template exposes it, or
- generate a static scene-specific HTML variant per frame.

A simple reliable trick for frame extraction is to duplicate the video HTML into per-scene files and make only one scene active at a time:
- `scene1.html` → only scene 1 marked active
- `scene2.html` → only scene 2 marked active
- etc.

This avoids depending on a click handler or animation timing during screenshot capture.

## Verification

After capture:
- run `file /path/to/output.png`
- confirm dimensions match the target aspect ratio
- if the output is for Telegram, attach the caption text separately and verify the caption file exists before sending

## Pitfalls

- `page.screenshot: Target crashed` usually means the browser runtime is unstable; try direct headless Chromium with `--no-sandbox`.
- `chromium: command not found` means the generic binary is absent; use the snap path or install the correct package.
- For `file://` pages, directory permissions and Chromium sandboxing can matter.
