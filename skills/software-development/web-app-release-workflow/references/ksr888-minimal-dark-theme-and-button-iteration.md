# KSR888 minimal dark theme + button iteration

Context:
- Imported PHP host: `/root/nusantara-ai-saas/KSR888/site`
- Live host: `https://ksr888.online`
- Goal: black-clean theme, white elegant text, subtle/ minimal button motion, without breaking DB connectivity or asset paths.

What worked:
- Put final visual overrides at the end of:
  - `site/dekstop/Content/Theme/dekstop.css`
  - `site/mobile/Content/Theme/mobile.css`
- Prefer a minimal override set:
  - `background-color: #000 !important;`
  - `color: #fff !important;`
  - buttons with translucent white fills/borders
  - hover = slight lift + lighter white tint
  - banner dots = subtle fade pulse, not neon
- Keep animations restrained for the "minimal" variant:
  - no heavy shimmer gradients
  - no strong glow/shadow stacks
  - 1–2 small transitions max per control

Verification pattern:
1. `docker compose build ksr888-web`
2. `KSR888_DB_USER=... KSR888_DB_PASSWORD=... docker compose up -d --no-deps --force-recreate ksr888-web`
3. Fetch the live CSS directly with cache-busting query strings:
   - `/dekstop/Content/Theme/dekstop.css?v=minimal1`
   - `/mobile/Content/Theme/mobile.css?v=minimal1`
4. Confirm the CSS response contains the final minimal markers (e.g. `ksr-dot-fade`, `rgba(255,255,255,.05)`).
5. Confirm the pages still return `200`:
   - `/dekstop/index.php`
   - `/mobile/index.php`

Pitfalls:
- Browser automation may fail with Chromium `ProcessSingleton` / socket-directory errors in this environment; if that happens, stop retrying identical launches and use HTTP/CSS verification instead.
- PHP host rebuilds can silently revert to bad DB credentials if the web container is recreated without the live DB env from the database container.
- For visual-only theme changes, avoid touching banner/game logic; keep the patch scoped to theme CSS so deployment risk stays low.