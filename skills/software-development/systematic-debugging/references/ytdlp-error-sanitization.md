# yt-dlp error sanitization for YouTube-based features

Use this when a worker or API shells out to yt-dlp and the raw stderr is too noisy for the UI.

Observed pattern
- yt-dlp may emit warnings like:
  - `No supported JavaScript runtime could be found`
  - `No title found in player responses`
  - `Sign in to confirm you’re not a bot`
  - `Use --cookies-from-browser or --cookies`
- These can appear together in one failure and create a long, scary error block in the UI.

Recommended handling
1. Preserve raw stderr/stdout in logs for debugging.
2. Parse and classify the error before sending it to the client.
3. Prefer short, actionable messages:
   - bot/cookie block -> tell the user to provide cookies or use an authenticated source
   - JS runtime warning -> tell the user to install/enable a JS runtime or Deno
4. Do not expose the full yt-dlp transcript in the UI.
5. If multiple signatures match, prioritize the most user-actionable cause for the current step.

Example classification order
- `sign in to confirm you’re not a bot` / `cookies-from-browser` / `cookies` -> anti-bot/cookie message
- `No supported JavaScript runtime could be found` -> JS runtime message
- everything else -> trimmed raw message or generic failure

Why this matters
- It keeps the UI readable.
- It prevents users from confusing a warning with the actual root cause.
- It still leaves the raw output available for logs and regression tests.

Implementation notes from the YouTube Heatmap Clipper case
- Treat yt-dlp as an external dependency with two independent failure surfaces: metadata probe and download/render.
- If the project has both a vendor library and a thin worker wrapper, add the same yt-dlp arg injection to both call sites; otherwise one path can still fail after the other is fixed.
- Useful default precedence for a shared helper:
  1. `YT_DLP_COOKIES_FILE`
  2. `YOUTUBE_COOKIES_FILE`
  3. `data/youtube-cookies.txt` in the working tree
  4. `/app/data/youtube-cookies.txt` in the container
- A local `node` install can satisfy `--js-runtimes` as `node:/abs/path/to/node` when yt-dlp needs a JS runtime.
- Verify with a direct import/compile check plus a regression test that asserts the sanitized message and hidden raw stderr.
