# News → image → Telegram pipeline notes

Session pattern:
- Input may be a zip archive containing: `bot.js`, HTML template, `.env.example`, `package.json`.
- If `unzip` is unavailable, use `python3` + `zipfile.ZipFile(...).extractall(...)` to inspect/extract safely.
- Inspect the HTML template before wiring render logic; do not assume slots exist.
- For this session, the template was `genz.html` — a fixed 4:5 poster/card with a red top zone and white bottom zone — and the final output needed to be a PNG.
- The user wanted the hero/title text reduced to a very short label (1–3 words) and requested that source labels not appear in the final image.
- When available, image content should come from the news article itself or the article page OG image; otherwise use a topic-matched fallback image/icon.

Source/content handling:
- Use a feed/API or RSS fallback to collect candidate headlines.
- Filter early for taboo topics and obviously off-brand results before rewriting.
- Keep source labels out of the final rendered asset if the user wants a clean social post.

Render fallback ladder:
1. Try browser-based HTML rendering when dependencies are available.
2. If browser tooling is unavailable or unstable, fall back to a deterministic CLI render path.
3. In this session, `ffmpeg` with `drawbox`/`drawtext` produced a valid PNG when Puppeteer/browser rendering was unavailable.

Telegram delivery:
- Use `sendDocument` for PNG delivery.
- Keep token/chat_id in env/config only.
- Verify the API response contains `ok:true` before assuming delivery succeeded.
- For a manual test, send one file first with a caption, then scale to batches.

Useful verification checks:
- file exists and is PNG
- dimensions match the intended card format
- text is not clipped
- Telegram upload returns `ok:true`
