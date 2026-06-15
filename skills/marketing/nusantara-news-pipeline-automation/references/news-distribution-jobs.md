# News Distribution Jobs (session note)

## New default distribution pattern
- A daily all-in-one cron job is now used for Nusantara-AI News distribution.
- Job name: `nusantara-news-daily-distribution`
- Schedule: every 24h
- Purpose:
  - generate news with scoring/voting/backtest/history
  - render 5:4 Instagram asset
  - render 9:16 short video
  - upload YouTube Shorts via OAuth 2.0 when credentials exist
  - update article/news page output
  - send Telegram delivery only when both image and video exist
  - prepare Instagram/TikTok-ready assets/captions

## Telegram targets
- Primary target env:
  - `TELEGRAM_CHAT_ID`
- Optional public mirror targets:
  - `TELEGRAM_PUBLIC_CHAT_ID`
  - `TELEGRAM_PUBLIC_CHANNEL_NAME`
- Delivery rule:
  - never send partial media
  - skip the item if image or video is missing
  - public mirror is additive; it does not replace the primary target

## Current social posting reality
- Instagram and TikTok direct uploader tooling is not yet present in the repo.
- The pipeline currently produces:
  - ready-to-post assets
  - captions
  - report entries that state the output is ready-post, not fake-posted
- Do not claim direct Instagram/TikTok posting unless actual upload tooling is installed and verified.

## Verification reminders
- Build the repo after pipeline edits.
- Deploy the container after build.
- Verify Telegram delivery only after confirming both media files exist.
- Keep credentials out of logs and output.
