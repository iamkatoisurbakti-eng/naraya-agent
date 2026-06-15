# KSR888 live-debugging notes

## When to use
Use when a live PHP page loads but reports browser/network errors, hidden 404s, or slow render caused by remote assets.

## Signals observed in this session
- Home HTML contained multiple third-party game images that resolved to dead hosts or 403s.
- Example bad hosts:
  - `https://ugy8n1py.suzieurs.biz/...` → DNS failure
  - `https://img.wokakse.com/...` → DNS failure
  - `https://img.zhenqinghua.com/...` → 403 in some cases
- Hidden SEO/footer copy also contained broken external links (for example a malformed `heylink.me` URL).
- Some apparent route errors were simply missing entrypoints that needed redirects (`/slots/playtech` → `/slots`, `/fish-hunter` → `/fishing`).

## Fix pattern
1. Inspect the *served HTML* with `curl` first; do not trust the source tree alone.
2. Extract all `src`, `href`, and `data-src` URLs from the live page.
3. Probe each URL with `curl -I` or `curl -sS -o /dev/null -w ...`.
4. If third-party asset hosts are dead or flaky, keep appearance unchanged by serving a same-origin fallback:
   - add a proxy/controller that returns the original asset when healthy
   - fall back to a local placeholder or cached image when unhealthy
   - cache successful fetches server-side to reduce repeat latency
5. For dead internal routes that are only reached by old links, add redirect routes instead of redesigning UI.
6. Re-verify the exact same live page after deploy; confirm every discovered same-origin URL returns `200`.

## Verification commands used here
- `curl -A 'Mozilla/5.0' -sS https://ksr888.online/`
- parse HTML for `src=`, `href=`, `data-src=` values
- probe each URL with `curl -L -sS -o /dev/null -w '%{http_code} %{time_total}'`
- test internal redirects with `curl -L -o /dev/null -w '%{http_code} %{url_effective}'`

## Practical note
If a live page is noisy but you must not change appearance, prioritize functional fixes in runtime data/routes over cosmetic HTML rewrites. Server-side proxying is often the safest way to preserve layout while eliminating console/network errors.