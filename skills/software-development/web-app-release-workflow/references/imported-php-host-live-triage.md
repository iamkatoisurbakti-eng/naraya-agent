# Imported PHP Host Live Triage

Use this note for live PHP/MySQL hosts like KSR888 when the user asks for *error fixes* or *speed improvements* **without changing the appearance**.

## Rules of engagement
- Keep changes functional-only unless the user explicitly requests a visual redesign.
- Verify the exact live entrypoint the host actually serves (`/`, `/index.php`, `/mobile/`, `/dekstop/`, `/support`, etc.).
- Do not assume a healthy container means the public hostname is fixed.
- Prefer local DB/cache reads on initial render; move remote provider calls behind explicit refresh endpoints or scheduled sync jobs.

## What to inspect first
1. Rendered HTML from the live host.
2. Container status with `docker compose ps`.
3. Laravel/PHP logs inside the serving container.
4. Database-backed catalog rows when errors mention games/providers/images.
5. Asset URLs actually referenced by the live HTML, including DB-driven image paths.

## Common fixes that do not change appearance
- Cache catalog/provider rows for a short TTL instead of querying on every request.
- Proxy or normalize dead third-party image URLs through a same-origin route.
- Clear Laravel caches inside the live container when deploys do not show up.
- If Laravel throws `fopen(.../storage/framework/cache/data/...)` lock errors, recreate the cache directory tree inside the serving container and ensure it is writable before re-running the request.
- If route:list complains about a missing legacy controller, add a small compatibility controller or update the route to the new class before debugging deeper.
- Use `curl`/HTTP probes for verification when browser automation is blocked.
- If the page still feels slow, check for synchronous remote calls during render and move them off the critical path.

## Verification
- `docker compose ps`
- `curl -I https://<host>/`
- `curl -sS https://<host>/ | grep -E 'expected-marker'`
- Container log check for 500s or missing asset/provider URLs
- If browser tooling fails, prefer HTTP smoke over repeated Chromium retries

## Notes from the KSR888 session
- The homepage became cleaner and faster by reading `providers` + `games` from the database and caching the result.
- Provider images were safer when served through a local proxy/fallback instead of hotlinking unstable external URLs.
- Live verification worked best by checking the actual served HTML and container state, not by relying on the source tree alone.
- When the user says “jangan ubah tampilan”, keep the patch limited to routes, data access, caching, and asset resolution.
