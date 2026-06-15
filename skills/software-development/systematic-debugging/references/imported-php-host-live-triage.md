# Imported PHP Host Live Triage

Use this checklist when a live PHP+MySQL host is slow, error-prone, or returning 500s, and the user explicitly asked *not* to change the visual appearance.

## Session lessons
- Prefer fixing runtime/root-cause issues only; do not change CSS, spacing, copy, or component layout unless the user asks.
- On KSR888-style hosts, the real live entrypoint may be `/index.php` even when `/`, `/mobile/`, or `/dekstop/` behave differently.
- Apache docroot can be `/var/www/html/public`; verify the served path before assuming a file patch failed.
- If Playwright/Chromium fails with snap singleton/profile/socket-directory errors, stop retrying browser automation and use HTTP/Jest smoke checks instead.
- For Laravel cache clearing inside a live container, prefer an interactive PTY wrapper: `script -qec "php artisan optimize:clear" /dev/null`.
- If the app depends on MySQL/PDO/GD, verify the live container actually has the extension (`pdo_mysql`, `gd`) and the runtime DB env, not just the source tree.
- For asset changes, verify the exact served file with a cache-busting query and hash the origin response rather than trusting the browser.

## Minimal triage flow
1. Fetch the live page with a browser-like UA.
2. Check response code, redirects, and title/hero markers.
3. Inspect logs for the first real exception.
4. Verify container env, docroot, and PHP extensions.
5. Clear caches in-container if the code changed but the live output did not.
6. Re-check the live URL and one or two critical static assets.
