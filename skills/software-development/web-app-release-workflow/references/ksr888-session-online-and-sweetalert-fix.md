# KSR888 session-online + SweetAlert fix notes

## Symptom
Mobile/desktop pages produced 404s for:
- `/session/online`
- `assets/js/sweetalert2.min.js`

The live JS bundle was still pointing at the old endpoint/path, so the page looked healthy but emitted background errors.

## Fix pattern
1. Inspect the live bundle, not only source, when a PHP host is already deployed behind cache/CDN.
2. If an endpoint is redirected or missing, point AJAX directly at the concrete file path that exists on disk, for example:
   - `/session/online/index.php`
3. If a vendor asset moved, switch to an already-served host asset instead of inventing a new local path, for example:
   - `/backoffice/assets/libs/sweetalert2/dist/sweetalert2.min.js`
4. Add a cache-bust query string to the page script tags when stale JS is likely:
   - `?v=20260509fix2`
5. Redeploy and verify with direct HTTP probes for both the HTML and the exact asset/bundle URLs.

## Verification commands
- `curl -I https://ksr888.online/session/online/index.php`
- `curl -I https://ksr888.online/backoffice/assets/libs/sweetalert2/dist/sweetalert2.min.js`
- `curl -fsSL https://ksr888.online/mobile/ | grep -o 'bundles/Home/mobile.js?v=20260509fix2\|bundles/Deposit/mobile.js?v=20260509fix2\|/backoffice/assets/libs/sweetalert2/dist/sweetalert2.min.js'`
- `curl -fsSL https://ksr888.online/mobile/bundles/Home/mobile.js?v=20260509fix2 | grep -n 'session/online/index.php'`

## Pitfalls
- Updating only source PHP files is not enough if the deployed bundle still points to the old path.
- A `301` on a POST endpoint can hide the real bug; prefer a stable file URL for AJAX calls.
- Browser cache and edge cache can keep the stale bundle alive after deploy, so verify with cache-busted URLs.