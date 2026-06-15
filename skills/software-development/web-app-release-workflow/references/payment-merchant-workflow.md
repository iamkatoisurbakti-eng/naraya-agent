# Payment and merchant integration notes

Use this as the condensed support file for checkout, webhook, and merchant-payment changes in web apps.

## Core pattern
- Inspect current checkout routes, webhook handlers, and order tables first.
- Keep provider credentials in env only.
- Persist local order state, provider reference, status, and timestamps.
- Make webhook/status updates idempotent.
- Verify the live route and the real checkout/status round trip, not just a landing page.

## UI / routing pitfalls
- Keep public checkout and admin/billing paths separate when possible.
- If a route conflicts with a public directory or static path, use a non-conflicting URI.
- For static checkout pages, sync source, mirrors, and deploy artifacts together.
- Probe the exact host/route the user referenced before editing.
