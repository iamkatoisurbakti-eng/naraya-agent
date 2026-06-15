# Short overlay browser fallback

Session finding:
- `ffmpeg drawtext` can render boxed/garbled glyphs in the Shorts title overlay when the title contains punctuation or the font stack/fontconfig path is unstable.
- The reliable fallback is a browser-rendered transparent PNG overlay, then composited with `ffmpeg` over the raw video.

Working recipe:
1. Keep the Shorts layout source of truth in `templates/nusantara_shorts_9x16.html`.
2. Render a transparent 1080x1920 overlay PNG via the helper script `tmp/render_short_overlay.cjs`.
3. Launch Chromium headless with an explicit executable path when Playwright has no downloaded browser:
   - `/snap/bin/chromium`
   - args: `--no-sandbox --disable-setuid-sandbox`
4. Keep the title to 1–2 lines for Shorts; prefer a short headline instead of trying to force long titles into a text box.
5. Composite overlay + video with `ffmpeg` using a simple `overlay=0:0` filter.

Pitfall:
- Do not retry the exact same `drawtext` setup if a boxed character appears; switch to the browser overlay path instead.
