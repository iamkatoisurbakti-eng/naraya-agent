# Imported PHP Host Release Notes

Use this note when the repo contains a host-specific PHP/MySQL app alongside the main Node stack.

## What mattered in the KSR888 session
- The PHP host lived under its own service (`ksr888-web`) and its root page was edited in `KSR888/site/index.php`, not in the main Node app.
- The correct document root was `public/`; pointing at the wrong root produced the wrong page or a PHP fatal path.
- The PHP container needed live DB credentials from the database container (`KSR888_DB_USER` / `KSR888_DB_PASSWORD`). Compose defaults could yield `mysqli` access-denied even when the DB container itself was healthy.
- Missing `pdo_mysql` caused the classic `could not find driver` failure; adding the extension fixed the runtime.
- The most reliable smoke test was a browser-like `curl` against the public host plus a cache-busted request for the exact HTML/asset being changed.
- If Chromium automation was blocked by profile/singleton errors, fall back to HTTP verification and content grep rather than repeatedly relaunching the browser.

## Release pattern
1. Confirm the host-specific service and file root before editing.
2. Sync the live DB env into the PHP container.
3. Ensure the PHP runtime has the needed MySQL extension.
4. Redeploy the host-specific stack separately from the main Node app.
5. Verify the public HTTPS host directly, not only container health.
