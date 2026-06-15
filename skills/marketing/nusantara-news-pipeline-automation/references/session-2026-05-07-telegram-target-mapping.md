# Session note: Telegram target mapping for Nusantara-AI News

Date: 2026-05-07

## What happened
- The user asked for a Telegram-ready pack and then requested one-by-one publishing to the Nusantara News Telegram channel.
- The messaging tool's `list` output showed only:
  - `telegram:TEST` (group)
  - `telegram:Nusantara Ai` (dm)
  - `telegram:TEST / topic 225` (group)
- Sending with `target: "telegram"` resolved to the home channel `chat_id: -1003922584410` and reported `mirrored: true`.

## Operational rule
- For future Telegram publishing, verify the target list first and do not assume `telegram` is the desired public channel.
- If the public channel handle is not listed, confirm the intended target before posting.
- For copy/paste output, format each item as a single Markdown block with:
  - bold title
  - short caption
  - CTA URL on a separate line
  - hashtag line
  - media path line if relevant
