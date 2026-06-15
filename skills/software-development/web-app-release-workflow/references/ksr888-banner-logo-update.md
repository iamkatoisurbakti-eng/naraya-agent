# KSR888 banner/logo update notes

Scope
- Imported PHP host at `ksr888.online`.
- Public website logo is driven by `tb_web.logo` / `tb_web.icon_web` and rendered from `/assets/img/<filename>` across desktop, mobile, and backoffice.
- Homepage banners are sourced from `tb_banner` and from the deployed `/banner/` directory.

What worked in this session
- To replace the website logo with a supplied image, create a cropped transparent logo plus a square favicon/icon variant. For ChatGPT-style PNGs with wide transparent/shadow padding, crop by alpha threshold (for example alpha >= 10) instead of alpha > 0, then cap the logo width (900px worked) and generate a 512x512 icon.
- Copy the logo/icon into every path the mixed PHP/Laravel host may serve from:
  - `KSR888/site/assets/img/<new-logo>.png`
  - `KSR888/site/backoffice/assets/img/<new-logo>.png`
  - `KSR888/site/public/assets/img/<new-logo>.png`
  - `KSR888/site/public/backoffice/assets/img/<new-logo>.png`
  - `KSR888/site/public/storage/<new-logo>.png`
  - repeat for `<new-icon>.png`
- Keep the database rows aligned: `tb_web.logo`, `tb_web.icon_web`, `genral_settings.logo`, and `genral_settings.favicon` should point at the chosen filenames.
- Because Apache serves `/var/www/html/public` as docroot in this stack, files copied only to `site/assets/img` can still return 404 at `/assets/img/...`; mirror under `site/public/assets/img` and verify live URLs.
- For banner gallery images, copy the entire source folder `KSR888/banner/` into the PHP image at `/var/www/html/banner/` and let slider templates read from `/banner/...`.

Verification pattern
- Build and recreate `ksr888-web` after asset changes, then clear Laravel cache using a PTY fallback if needed:
  - `docker compose exec -T ksr888-web script -qec 'php artisan optimize:clear --no-ansi' /dev/null`
- Check these URLs directly with cache-busting and a browser-like User-Agent:
  - `/assets/img/<logo>`
  - `/assets/img/<icon>`
  - `/backoffice/assets/img/<logo>`
  - `/storage/<logo>`
  - `/storage/<icon>`
  - `/banner/<file>`
  - `/dekstop/index.php`
  - `/mobile/index.php`
  - `/backoffice/index.php` or `/support`
- Grep fetched live HTML for the new logo/icon filenames; a `200` asset alone does not prove the DB/template now references it.
- Prefer HTTP verification with a browser-like User-Agent when browser smoke is blocked.

Pitfalls
- Do not rely on local file placement alone; the PHP image must copy the new asset in Dockerfile or the file must be mirrored into the live container immediately and committed to source for the next rebuild.
- If `/storage/<logo>` works but `/assets/img/<logo>` returns 404, the file is likely missing from `site/public/assets/img` because the Apache docroot is `public`.
- If the web container returns 500 with `Access denied`, sync the live DB env from the DB container before recreating the web container.
- If `php artisan optimize:clear` fails with Symfony `StreamOutput` under non-interactive exec, rerun through `script -qec ... /dev/null`.
- If Chrome/Playwright fails with `ProcessSingleton` or socket-directory errors, switch to HTTP asset checks instead of retrying the same browser launch.
