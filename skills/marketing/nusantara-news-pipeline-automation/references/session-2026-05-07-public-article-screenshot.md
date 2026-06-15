# Public article verification, screenshot, and Telegram report

Session learnings:
- Public article detail pages can be verified before screenshot by hitting the JSON API directly:
  - `curl -kfsS https://news.nusantara-ai.online/api/news/articles/<category>/<slug>`
- If the page shows `Gagal memuat artikel berita`, the UI is live but the article payload is missing or not synced into the container volume.
- In this session, syncing `/root/nusantara-ai-saas/data/news-articles` into the running container with `docker compose cp data/news-articles app:/app/data/news-articles` fixed the public article detail endpoint.
- `browser_navigate` timed out repeatedly on the public URL, so a system Chromium screenshot was more reliable than browser-tool navigation.
- Playwright was installed in Node but lacked a browser binary; `npx playwright install chromium` failed on Ubuntu 26.04 with an unsupported platform error.
- The system Chromium snap worked for screenshots:
  - `/snap/bin/chromium --headless --disable-gpu --no-sandbox --hide-scrollbars --window-size=1440,2200 --screenshot=/root/nusantara-news-article.png '<article-url>'`
- After screenshot verification, send a short Telegram report with the public URL, title, category, and the screenshot path.
- If screenshot verification fails, do not claim the article is public-ready yet; verify the JSON API first and fix the data sync or route before sending a report.
