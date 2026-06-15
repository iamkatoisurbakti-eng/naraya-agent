# KSR888 Live Debugging Notes

This note captures the pattern used when the KSR888 homepage was slow or error-prone.

## Observed pattern
- The public homepage can look fine in source but still be slow because it renders DB-backed provider/game data on every request.
- The biggest visible errors were usually not in the HTML shell, but in runtime data: missing provider rows, stale image URLs, or remote asset hotlinks.
- A live check of the rendered HTML was more useful than inspecting source alone.

## What worked
- Read `providers` and `games` from the database as the source of truth.
- Cache the combined catalog briefly for the homepage so repeated requests are cheap.
- Proxy provider images through same-origin URLs or a local fallback when external URLs are unstable.
- Keep the page appearance unchanged; only change data flow, caching, and asset resolution.

## Live verification
- Confirm the homepage returns `200`.
- Grep live HTML for the expected section markers.
- Verify `docker compose ps` shows the PHP container healthy.
- If browser automation is blocked by Chromium snap/profile issues, use HTTP smoke checks instead.

## Pitfalls
- Do not assume the source tree matches the live runtime; verify the served HTML.
- Do not hotlink unstable third-party assets if they are already stored in local DB rows.
- Do not add visual changes just to hide a runtime/data problem.
