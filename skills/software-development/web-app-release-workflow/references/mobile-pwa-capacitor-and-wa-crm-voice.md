# Mobile PWA + WA CRM Voice Notes

Session-specific notes for Nusantara AI mobile readiness and WhatsApp CRM voice UX.

## What worked
- Add a PWA shell first:
  - `manifest.webmanifest`
  - SVG icons + maskable variant
  - `apple-touch-icon` and favicon links in `web/index.html`
- Keep Capacitor as a second step after the web app builds cleanly.
- Verify `npm run build:web` before moving to native wrapper work.

## WA CRM voice UX pattern
- Give the user a dedicated `WA CRM` dashboard entry instead of hiding voice inside generic chat.
- Keep voice as a deterministic parse-and-route layer before heavier AI:
  - add contact
  - create follow-up
  - draft reply
  - summarize conversation
  - log note
- Include sample voice commands and a plain transcript textarea so users can type if mic access is not available.
- Show structured output cards: contact, follow-up, draft reply, suggested actions, confidence.

## Usability pattern
- Add a `Panduan`/getting-started card for first-time users.
- Prefer 1-2-3 steps, quick-start chips, and short labels like `Template`, `Evaluasi`, `Jasa`, `WA CRM`.
- For template panels, include prompt + caption + hashtag copy buttons so users can reuse content quickly.
- For evaluation panels, keep upload + score + strengths/weaknesses + next steps in one screen.
