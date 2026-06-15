# Signed-in free Chat AI + Clipper

Session note:
- Product rule: once a user registers/signs in, Chat AI and Clipper are free.
- Chat AI should stay on one free path in the UI; no model selector for the chat experience.
- Clipper should be accessible without paid subscription gating for authenticated users.
- Customer-facing copy should stay simple: "Chat gratis", "Chat AI gratis", and "Clipper gratis". Avoid provider labels like "Provider Ark Chat • Gratis" in the visible UI.
- When credit cost is zero, show a plain free state instead of a credit amount badge.
- Verification that worked: build + API tests + deploy + authenticated live smoke test proving both chat and clipper routes are accessible without subscription.

Implementation pattern that worked:
- Backend: whitelist clipper in subscription access checks and set clipper credit cost to 0.
- Frontend: show a free badge only when cost is zero; hide any confusing provider wording.
- Tests: add a focused access-rule unit test plus an API smoke test that proves the two free paths still work after deploy.
