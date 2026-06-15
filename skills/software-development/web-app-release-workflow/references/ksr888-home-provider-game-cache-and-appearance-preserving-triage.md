# KSR888 home provider/game cache + appearance-preserving triage

## Session takeaway
When a live imported PHP host needs faster loading and fewer runtime errors, keep the patch functional-only:
- do not change public appearance unless explicitly requested
- inspect the live HTML first, then the DB-backed source of truth
- move expensive provider/game assembly behind server-side cache
- proxy external provider images instead of hot-linking them directly
- verify the live host with `curl`/HTML grep plus container status when browser automation is flaky

## KSR888-specific pattern
- Homepage source of truth is the live DB tables `providers` and `games`
- Homepage provider/game catalogs were cached server-side to reduce repeated work on every request
- Provider images can be overridden from the API and proxied via same-origin URLs to avoid slow or brittle external fetches
- Category cards should use a single `detail_url` mapping so homepage and category pages stay consistent

## Verification pattern
1. `curl https://ksr888.online/` and grep for the expected section labels/links
2. `curl` the category pages to confirm cards point to the correct route family
3. Check `docker compose ps` after deploy so the PHP web container is healthy
4. If browser automation is blocked, prefer HTTP verification over repeated Chromium retries
