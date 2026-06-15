# News subdomain and branding notes

Use this when exposing a public article/news surface on a separate host such as `news.nusantara-ai.online`.

## Key decisions
- Public host should render only the news/article experience.
- Non-news routes on the news host should redirect to `/news`.
- Backend/API can stay shared, but CORS must allow every browser origin that serves the app (comma-separated `CLIENT_ORIGIN` is a simple pattern).
- Public article pages should be branded `Nusantara-AI News`.
- Do not render source/sourceLabel/source names in public UI; keep them internal only.
- If article metadata still carries source fields, use them for storage or fallback URLs, not for visible labels.

## Practical routing pattern
- Detect the host in the SPA with `window.location.hostname`.
- If host matches the news subdomain, mount a news-only router.
- Keep the regular app routes on the primary host.

## Verification
- Check the news host opens the news index directly.
- Check dashboard/admin routes are not exposed on the news host.
- Check article cards and detail pages do not show source labels.
- Check API requests still succeed from the news host (CORS).
