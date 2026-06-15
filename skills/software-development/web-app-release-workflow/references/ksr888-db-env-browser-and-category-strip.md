# KSR888 DB env, browser fallback, and category-strip notes

Use this note when working on the imported KSR888 PHP host.

## Live DB env sync
- The web container must inherit the live DB credentials from the running DB container.
- The imported PHP app reads plain `DB_HOST/DB_NAME/DB_USER/DB_PASSWORD/DB_PORT` at runtime, but the Compose service also needs the live `KSR888_DB_*` values available so container recreation does not fall back to defaults.
- A stale container can present as `mysqli_sql_exception: Access denied for user 'ksr888_user'@'172.18.0.4'` even when the DB container itself is healthy.
- Verify the effective env inside the recreated container with `docker inspect <web-container> --format '{{range .Config.Env}}{{println .}}{{end}}' | sort | grep '^DB_'` and then smoke-test `mysqli_connect(...)` or the public page.

## Browser verification fallback
- Chromium/Playwright can fail with `ProcessSingleton` / socket-directory errors when a stale profile directory exists under `/tmp`.
- Do not retry the same browser launch unchanged.
- Clean stale profile dirs first; if browser automation still fails, fall back to live HTTP verification with a browser-like UA and grep for the new CSS markers.

## Category-strip tuning for KSR888
- Use end-of-file CSS overrides for menu/category strips so the imported PHP markup stays intact.
- The banner reference can change the palette and motion:
  - `banner/4.png` → dark strip with pink/magenta glow
  - `banner/3.png` → dark strip with green/gold fantasy glow
- Keep the changes in CSS, not template rewrites, unless the markup itself is broken.
- Always bump the stylesheet cache-buster in the PHP entry page after updating the theme file.

## Verification
- Confirm the live page returns 200.
- Confirm the active stylesheet URL includes the new cache-buster token.
- Confirm the CSS response contains the new markers for the chosen banner-inspired strip.
- If the page 500s, check the container env first before editing CSS again.