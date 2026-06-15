# Landing news widget + feature CTA pattern

Use this when the homepage should preview news and steer users into the app's main features.

## Pattern
- Fetch a small preview set from the internal news proxy, typically `GET /api/news?source=all&limit=3`.
- Keep the landing widget read-only and light-weight; do not expose provider internals in the public UI.
- Prefer placing the widget early on the landing page, before the main showreel/studio sections, so it feels current without replacing the core product pitch.
- Use a compact two-column layout when space allows: news preview on one side, feature CTAs on the other.
- Provide clear CTA chips/buttons to the app's main anchors or dashboard entry points, such as:
  - images studio
  - video studio
  - music studio
  - voice agent
  - AI clipper
  - AI chat
  - VIP / billing
- Show a loading skeleton and a friendly error state if the news fetch fails.
- Keep article cards minimal: image, source, category, title, summary, outbound link.

## Verification
- Run the app typecheck after patching JSX around the landing page.
- If the landing page uses anchor navigation, verify the anchor ids still exist before wiring CTAs.
- Prefer internal API helper calls instead of raw `fetch` so the client stays aligned with app auth/base-URL handling.

## Pitfalls
- Avoid hardcoding external feed URLs in the browser bundle.
- Don't let the widget become a full news page; it should point users to the deeper dashboard/news experience.
- If the landing page section order changes, re-check the widget placement so it still appears before the main studio/showreel block.
