# yt-dlp YouTube anti-bot / JS runtime fallback

Use this when YouTube extraction fails with any of these signals:
- `No supported JavaScript runtime could be found`
- `Sign in to confirm you’re not a bot`
- `Use --cookies-from-browser or --cookies`
- HTTP 429 / temporary rate limit / anti-bot messages

Observed behavior in this repo:
- `yt-dlp` is used for metadata, duration, and clip downloads in the heatmap clipper.
- The container already has `node` available, so `--js-runtimes node:/usr/bin/node` can be passed to yt-dlp.
- If anti-bot still blocks extraction, a Netscape cookie file must be present at `/app/data/youtube-cookies.txt` (mounted from the `data` volume) or supplied via `YT_DLP_COOKIES_FILE` / `YOUTUBE_COOKIES_FILE`.

Recommended order:
1. Add JS runtime first: `--js-runtimes node:/usr/bin/node` (or env override `YT_DLP_JS_RUNTIMES`).
2. If the error persists, use cookies from a logged-in browser session.
3. Prefer a persistent file path in the app data volume, not a one-off host path.
4. Keep the failure message user-friendly; do not surface the raw yt-dlp warning block in the UI.

Implementation notes:
- Common yt-dlp args should be centralized in one helper so metadata/duration/download calls all inherit the same runtime/cookie config.
- If the app exposes a UI for cookie upload, save Netscape text verbatim to the mounted data path.
- In containers, `node` may exist on the host but not inside the runtime; verify inside the running container before relying on it.

Verification checklist:
- Confirm `yt-dlp --help` shows `--js-runtimes` and `--cookies` support in the runtime container.
- Confirm a simple helper returns `['--js-runtimes', 'node:/usr/bin/node']` when `node` is present.
- Confirm the cookie save endpoint writes `/app/data/youtube-cookies.txt` and the file is visible in the container.
- Run the clipper regression tests for bot-block sanitization and cookie persistence.
