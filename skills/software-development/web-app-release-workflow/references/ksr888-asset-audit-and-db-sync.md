# KSR888 asset audit and DB sync

Use this note when cleaning imported PHP app pages such as KSR888 desktop/mobile/backoffice.

## What worked
- Audit rendered pages by fetching the live HTML and extracting `src`, `href`, `srcset`, CSS `url(...)`, and inline image references.
- Recheck each discovered asset URL with HTTP status. Count 200 vs bad resources so success is evidence-based, not visual guesswork.
- Replace dead CDN/Cloudfront references with local assets under the same host when possible.
- For PHP pages behind a proxy, verify the exact public file with a cache-busting query string after the patch.
- If the app uses a Dockerized PHP web container, recreate it with the live DB env from the database container; default compose credentials can cause `mysqli` access-denied even while the DB container is healthy.
- Smoke-test DB connectivity inside the web container before chasing UI bugs.

## KSR888-specific examples
- Desktop modal popup assets were redirected from dead CDN references to local backoffice assets.
- Mobile favicon/logo references were rewritten to the domain-local asset path.
- A typo like `https:<?= $urlweb; ?>...` can silently double the scheme and break image downloads.
- After fixes, verify the page plus all discovered resources return HTTP 200.

## Verification pattern
1. Fetch page HTML.
2. Parse resource URLs.
3. Probe each URL with HTTP.
4. Recreate the web container if DB auth is suspect.
5. Re-run the page and resource check after deploy.