# KSR888 admin setting visibility + QRIS-only deposit

Session note for the imported PHP host workflow on `ksr888.online`.

## Admin setting visibility
- The real admin login surface used in this session was `https://ksr888.online/support`.
- Successful admin authentication should land on `/dashboard`.
- If `/setting` exists in the code but is hidden behind a developer-only branch, move the route into the admin-visible group and add the sidebar link instead of editing the view alone.
- Verify the live page with the actual host/path after deploy; a healthy container is not enough.

## QRIS-only deposit simplification
- To make deposit QRIS-only without changing appearance, hide or remove every alternate method from the rendered templates, not just one screen.
- The affected KSR888 surfaces in this session were:
  - `mobile/template/menu/deposit.php`
  - `dekstop/template/menu/deposit.php`
  - `resources/views/account/deposit.blade.php`
- Confirm the live HTML on both mobile and desktop routes only exposes the remaining QRIS method.
- If browser automation is unreliable on the host, use HTTP/curl verification against the live routes.

## Runtime hygiene
- Keep the patch functional-only when the user explicitly says not to change the appearance.
- Clear Laravel cache in-container if the live HTML looks stale after deploy.
- When the host already serves cleanly, prefer route/menu exposure fixes over layout rewrites.