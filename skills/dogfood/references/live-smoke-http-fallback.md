# Live smoke HTTP fallback

Use this when browser automation fails or is unavailable on the host.

## When to switch
- Chromium/Playwright fails with `ProcessSingleton`, profile-lock, or DevToolsActivePort errors.
- Browser launch loops repeat the same failure.
- You only need to verify live routes, redirects, asset availability, or response errors.

## Minimal probe set
1. `curl -k -sS -L -o /tmp/body.html -w '%{http_code} %{time_total} %{url_effective}' https://TARGET/route`
2. Inspect body for fatal markers:
   - `Fatal error`
   - `Parse error`
   - `SQLSTATE`
   - `Exception`
   - `Warning:`
   - `Notice:`
3. Check for stale branding/error strings with `grep` or regex against the saved HTML.
4. HEAD critical assets and endpoints:
   - `curl -k -I -sS -o /dev/null -w '%{http_code} %{time_total}' URL`
5. For many asset URLs, use a small script (Python `requests.head` works well) to batch-check status codes.

## What to record
- HTTP status
- Effective URL after redirects
- Response time
- Visible error strings in HTML
- Asset/route non-200s
- Any unexpected 404/500/302 loops

## Notes from KSR888 session
- Public routes can return `200` while hidden asset URLs still 404; check the HTML for embedded asset references.
- A missing or malformed absolute URL like `https:///` can appear in templates and should be replaced with `#` or a valid URL.
- If a route like `/mobile/` or `/dekstop/` is expected to exist, verify both with and without trailing slash and with `index.php` variants.
- It is useful to add redirect shims for dead legacy entrypoints rather than changing the visual layout.
