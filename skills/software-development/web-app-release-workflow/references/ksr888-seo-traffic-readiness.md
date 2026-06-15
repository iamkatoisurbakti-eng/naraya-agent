# KSR888 SEO / traffic readiness audit

Use this when evaluating `ksr888.online` or similar PHP-hosted releases for SEO/traffic readiness before deciding whether changes are allowed.

## Gate
- If the user gives a numeric score threshold, treat it as the release gate exactly.
- In the May 2026 KSR888 session, changes were allowed only when the audit score was above 50.

## What to check live
1. Fetch the public URLs directly with a browser-like user agent.
2. Confirm HTTP 200 for:
   - `/sitemap.xml`
   - desktop entry page
   - mobile entry page
3. Inspect HTML for:
   - canonical URL correctness
   - meta description presence and relevance
   - meaningful H1/H2 copy
   - `alt` text on key images/icons
4. Extract `src`/`href`/CSS `url(...)` references and probe them directly.
5. If assets look stale, request the exact public file with a cache-busting query string before judging the deploy.

## KSR888 specifics learned
- Sitemap was added at `/sitemap.xml` with the root, desktop, and mobile URLs.
- Desktop/mobile canonical tags were normalized to `https://ksr888.online/`.
- Desktop got SEO hero copy; mobile got stronger footer copy and alt text for menu icons.
- Live verification was done after build/recreate, not just after source edits.
- The host-specific PHP container once failed on DB access because the web container env did not match the live DB container; a recreate with the correct env fixed the issue before SEO changes were meaningful.

## Verification pattern
- Build/recreate the web container.
- Re-fetch the public URLs with `curl`/Python and confirm the expected strings are present.
- If browser automation is flaky, fall back to direct HTTP checks and cache-busted asset probes.
- Do not treat build success alone as proof of public readiness.