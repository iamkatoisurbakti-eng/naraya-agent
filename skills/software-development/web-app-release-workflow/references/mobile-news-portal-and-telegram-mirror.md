# Mobile news-portal layout and Telegram mirror pattern

Use this note when the request is about making the news surface feel like a portal/majalah on mobile, or when a run should mirror generated assets to Telegram.

## Mobile news-portal layout
- On small screens, keep the hierarchy editorial and low-clutter:
  - masthead first
  - one dominant cover story
  - compact breaking-line / editor's pick rail
  - category chips in a horizontal scroll row, not wrapped into a tall block
- If the headline clips on narrow widths, split it with explicit line breaks instead of shrinking everything.
- Hide or soften heavy hero video/media on phones when it hurts readability or performance.
- Prefer stacked CTAs on very narrow widths.
- Keep article/news cards single-column on phones and reduce image height.
- Add small global usability tweaks when needed:
  - `overflow-x: hidden`
  - `touch-action: manipulation`
  - modest `scroll-padding-top`
- Verify with a real mobile viewport screenshot, for example Chromium headless at `390x844`, and inspect for:
  - clipped text
  - wrapped buttons
  - cramped chips
  - horizontal overflow

## Telegram mirror for generated news outputs
- If the user wants public Telegram mirroring, send both files for each item:
  - image 5:4 first
  - then the final video
- Keep the existing safety rule: if either image or video is missing, skip that item entirely.
- Support multiple targets by reading a primary chat plus a public mirror chat from env vars.
- Keep captions short and reuse the story title + concise summary; cap caption length to avoid API rejections.
- Treat Telegram group/channel IDs and bot tokens as secrets; never echo them back in logs or chat.

## Operational reminder
- The same generated story can be mirrored to private and public Telegram targets, but the public mirror should still be fed from the same final image/video pair so the output stays synchronized.
