# 2026-05-07 notes: public news posting, YouTube OAuth, and Telegram-ready test

Session learnings for Nusantara-AI News automation:

- Public article posting is already handled by `scripts/genz-news.ts` via `saveGeneratedNewsArticles(...)`, which writes `data/news-articles/**` consumed by `src/routes/news.ts` and the public site `news.nusantara-ai.online`.
- For public-facing captions/reports, normalize relative article paths like `/news/<category>/<slug>` to a full URL using `NEWS_PUBLIC_BASE_URL=https://news.nusantara-ai.online`.
- Add/ensure `NEWS_PUBLIC_BASE_URL` in `.env` and `.env.example`; it is non-secret.
- Before claiming public posting works, verify with an HTTP HEAD/GET against the exact article URL, e.g. `curl -kfsSI https://news.nusantara-ai.online/news/<category>/<slug>`.
- YouTube refresh token flow used a repo helper `scripts/youtube-oauth-refresh-token.ts` exposed as `npm run youtube:oauth`:
  - `npm run youtube:oauth -- --auth-url`
  - user approves in browser; if Google says app is in testing, add the Gmail/channel account as an OAuth Test user in Google Cloud Auth Platform → Audience.
  - exchange redirect URL with `npm run youtube:oauth -- --code "http://localhost/?code=..."`
  - store `YOUTUBE_REFRESH_TOKEN` without printing it.
- `.env` validation should repair common paste mistakes before live-starting. Observed example: `TELEGRAMBOT:<token>` should become `TELEGRAM_BOT_TOKEN=<token>`.
- Test request pattern: “buat 1 video siap upload ke youtube dan instagram kirim ke telegram” should usually run one pipeline item without YouTube upload unless the user explicitly asks to publish live:
  - `NEWS_MIN_SCORE=90 NEWS_MIN_SINGLE_SCORE=90 NEWS_INSTAGRAM_ASPECT=4:5 NEWS_NATURAL_NARRATION=1 npm run gen:news-pipeline -- --count 1 --skip-youtube`
  - This creates public article + Instagram 4:5 image + 9:16 video + Telegram send after both image and final video exist.
- Do not report Telegram sent until final video exists, Telegram API send succeeds, and `pipeline-report.json` marks `telegramSent: true`.
