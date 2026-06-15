# KSR888 admin dashboard live GameXa cards + asset persistence

## Trigger
Use when KSR888 admin dashboard cards need to show live GameXaGlobal data, or when new logo/banner assets must survive rebuilds and appear immediately on the public/admin site.

## Live dashboard cards pattern
- Keep legacy provider cards out of the admin dashboard once GameXaGlobal is the active source. Remove the UI card, JS fetch, route, controller method, and stale cache key together.
- For live GameXaGlobal card data, add auth/admin-protected JSON endpoints on `BackofficeController` and route them in the admin group:
  - `/get-balance` for live agent balance from `gamexaglobal()->me()` / `/api/auth/me`
  - `/dashboard/game-api-summary` for all-provider/game counts from `/api/games/providers` and `/api/games?limit=1&page=1`
- Return realtime response metadata and no-cache headers:
  - `provider: GameXaGlobal`
  - `realtime: true`
  - `server_time`
  - `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`
  - `Pragma: no-cache`
- In `resources/views/admin/backoffice.blade.php`, fetch with:
  - `cache: 'no-store'`
  - query timestamp like `?_=` + `Date.now()`
  - `credentials: 'same-origin'`
  - clear status text such as `Live GameXaGlobal • active • <server_time>`
- Refresh cadence used successfully:
  - Agent balance: 10 seconds
  - Game API summary: 30 seconds

## Payload gotchas
- GameXaGlobal `/api/auth/me` can return `agent.balance` directly. Probe fallbacks: `balance`, `data.agent.balance`, `data.balance`.
- `/api/games/providers` returned keys `success, providers, total`; use `total` for provider count.
- `/api/games?limit=1&page=1` returned keys `success, total, games`; use `total` for game count.
- In live verification, protected dashboard JSON routes return `302` without admin session; treat that as normal auth protection, then verify the upstream GameXa API directly from the container and grep deployed source for the new route/UI code.

## Asset/logo/banner persistence pattern
- For a user-supplied KSR888 logo PNG with transparency, crop using the alpha channel threshold rather than the raw alpha bbox. Raw bbox may include low-alpha shadow over the whole canvas. A threshold around alpha >= 10 gave a usable horizontal logo crop.
- Save logo/icon mirrors to all relevant source paths before rebuild:
  - `site/assets/img/`
  - `site/backoffice/assets/img/`
  - `site/public/assets/img/`
  - `site/public/backoffice/assets/img/`
  - `site/public/storage/`
- Update both DB sources when replacing the live logo:
  - `tb_web.logo`, `tb_web.icon_web`
  - `genral_settings.logo`, `genral_settings.favicon`
- For homepage banners, add files to `site/public/storage/post-images/` and insert active rows in `banner` with `gambar='post-images/<file>'`, not only `/banner/`; the Laravel homepage uses `asset('storage/' . $banner->gambar)`.

## Deploy and verification
1. PHP lint changed files before rebuild.
2. Rebuild/recreate `ksr888-web` with production env loaded.
3. Clear Laravel cache; if `php artisan optimize:clear` fails with Symfony `StreamOutput`, rerun with a real PTY or `script -qec` depending on which mode works in that shell.
4. Restart Caddy.
5. Verify:
   - `docker compose ps`
   - DB connect from `ksr888-web`
   - direct GameXa API status/totals without printing tokens
   - public `/support` 200
   - protected admin routes 302 unauthenticated, 404 for removed legacy routes
   - grep deployed container source for UI labels/routes
   - recent logs have no fatal/parse/syntax/SQL/access denied/type errors
