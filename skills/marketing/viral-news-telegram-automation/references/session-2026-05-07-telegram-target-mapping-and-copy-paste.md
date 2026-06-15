# Session note: Telegram target mapping and per-item copy-paste

Date: 2026-05-07

## What happened
- User asked for a Telegram-ready format that can be copied item-by-item, then asked to send 10 flyer posts one by one.
- The available messaging targets list showed only:
  - `telegram:TEST` (group)
  - `telegram:Nusantara Ai` (dm)
  - `telegram:TEST / topic 225` (group)
- Sending with `target: "telegram"` resolved to the home channel `chat_id: -1003922584410` and returned `mirrored: true`.

## Learning
- Do not assume bare `telegram` means the user’s intended public channel.
- Always inspect `send_message list` targets first when the user asks to send to a specific Telegram destination.
- If the exact channel/handle is not listed, clarify the intended target or use the mapped home channel only if that is explicitly acceptable.
- For "tinggal copas" requests, provide a per-item block with:
  - bold title
  - caption paragraph
  - CTA URL on its own line
  - hashtag line
  - media path line

## Practical pattern
1. Generate/collect per-item copy blocks in Markdown.
2. Verify the target list before sending.
3. Send one item at a time to the exact destination.
4. Confirm success after each send, especially when mirroring is involved.
