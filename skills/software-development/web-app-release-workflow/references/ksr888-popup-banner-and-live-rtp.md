# KSR888 popup banner and LIVE RTP link updates

Use this reference when KSR888 requests popup/banner swaps or external LIVE RTP routing.

## Popup banner swap pattern
1. Copy the user-provided image into the served public location:
   - `KSR888/site/public/uploads/fotobanner/<new-file>.png`
   - keep names simple and cache-bust in Blade, e.g. `popup-banner-YYYYMMDD.png?v=YYYYMMDDa`.
   - The Docker image copies `KSR888/site/` into `/var/www/html/`; a separate host `KSR888/site/uploads/...` copy is not required unless legacy non-public code references it.
2. Check `resources/views/content/popup_banner.blade.php` first. It may have been intentionally reduced to a disabled comment; in that case, re-enable the partial rather than hunting for a database renderer.
3. For a simple static popup, render a fixed overlay with close button, image link to `url('/daftar')`, and Escape/outside-click close behavior. Use a public asset path such as `asset('uploads/fotobanner/<new-file>.png') . '?v=...'`.
4. If the live implementation uses `tb_popup`, update `tb_popup` carefully: `tb_popup.status` is numeric (`1` active), not the string `active`; using `'active'` causes MySQL `Incorrect integer value`.
5. Desktop and mobile layouts already include `content.popup_banner`; verify both `/` and `/slots` for popup markers instead of adding duplicate includes.
6. Clear compiled views after deploy. Prefer normal `php artisan optimize:clear --no-ansi && php artisan view:clear --no-ansi`; if artisan console is unreliable, fall back to removing compiled files: `rm -f storage/framework/views/*.php bootstrap/cache/*.php || true`.

## LIVE RTP link routing pattern
1. Search rendered HTML when code search misses text. For KSR888, `/` rendered the floating menu from `resources/views/content/outer.blade.php` even when `search_files` did not find `RTP` initially.
2. Update both the visible href and route fallback:
   - Floating RTP href in `resources/views/content/outer.blade.php`
   - `/rtp-gacor` route in `routes/web.php` using `redirect()->away('https://target/')`
3. Smoke test:
   - `curl -I https://ksr888.online/rtp-gacor` should show `Location: https://target/`
   - fetch `/` and assert the new external href exists and the old internal href is absent
   - `curl -I https://target/` should return 200/3xx

## Verification checklist
- `file`/`identify` the source image before copying, then `php -l` the popup Blade source.
- `docker compose build ksr888-web` from `/root/nusantara-ai-saas`; the app source is copied into the image and is not bind-mounted live.
- Recreate the web container with the rebuilt image. If the terminal tool flags `docker compose up -d --no-deps ksr888-web` as long-running, run it in the background and wait for completion.
- After the new container starts, clear Laravel views/cache normally (avoid redirecting artisan output to `/dev/null` in this container; it can trigger a Symfony Console stream error).
- Runtime checks:
  - `test -f /var/www/html/public/uploads/fotobanner/<new-file>.png` inside the container.
  - live asset URL returns `200` and the expected PNG dimensions/bytes.
  - live `/` and `/slots` contain the new filename plus `ksrPopupBanner`/popup overlay markers for desktop and mobile user agents.
  - `docker logs --tail` shows no fresh PHP fatal errors.
