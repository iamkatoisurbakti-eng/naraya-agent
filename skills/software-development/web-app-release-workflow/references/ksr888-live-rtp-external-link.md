# KSR888 LIVE RTP / RTP GACOR external link wiring

Use when the user asks to connect the KSR888 LIVE RTP / RTP GACOR button to an external site.

## Surfaces
- Source repo: `/root/nusantara-ai-saas/KSR888/site`
- Deploy from: `/root/nusantara-ai-saas`
- Floating home RTP button source: `resources/views/content/outer.blade.php`
- Fallback route source: `routes/web.php`

## Fix pattern
1. Search for RTP labels and routes in both Blade and route files:
   ```bash
   grep -RIn "rtp-gacor\|RTP GACOR\|LIVE RTP\|miebakso" routes resources/views 2>/dev/null
   ```
2. Update the visible floating RTP link in `resources/views/content/outer.blade.php` directly to the external URL, e.g.:
   ```blade
   <a href="https://miebakso.store/" target="_blank" rel="noopener nofollow">
   ```
3. Keep `/rtp-gacor` as a fallback route but redirect externally:
   ```php
   Route::get('/rtp-gacor', function () {
       return redirect()->away('https://miebakso.store/');
   });
   ```
4. Do not route through `/promotion` if the user asked to connect LIVE RTP directly to another host.

## Verification
- Syntax:
  ```bash
  docker compose exec -T ksr888-web bash -lc 'php -l routes/web.php && php -l resources/views/content/outer.blade.php'
  ```
- Build/deploy/restart:
  ```bash
  docker compose build ksr888-web
  docker compose up --no-build -d ksr888-web
  docker compose restart ksr888-web
  ```
- Clear Blade cache manually if artisan stream output fails:
  ```bash
  docker compose exec -T ksr888-web bash -lc 'rm -f storage/framework/views/*.php bootstrap/cache/*.php || true'
  ```
- Live smoke:
  ```bash
  curl -k -sS -I https://ksr888.online/rtp-gacor | sed -n '1,12p'
  curl -k -sS https://ksr888.online/ -o /tmp/ksr_home_rtp.html
  python3 - <<'PY'
  from pathlib import Path
  s = Path('/tmp/ksr_home_rtp.html').read_text(errors='ignore')
  print('external link:', 'https://miebakso.store/' in s)
  print('old direct rtp link:', 'href="https://ksr888.online/rtp-gacor"' in s or 'href="/rtp-gacor' in s)
  PY
  curl -k -sS -I https://miebakso.store/ | sed -n '1,8p'
  ```
Expected: `/rtp-gacor` returns `302` with `Location: https://miebakso.store/`, home HTML contains the external URL, and the external target is reachable.

## Pitfalls
- `search_files` may return zero for short/uppercase terms; verify using Python or grep when the live HTML clearly contains `RTP`.
- Do not remove the floating RTP item unless the user asks; only change its `href` and keep label/icon intact.
- Treat external target reachability separately from KSR888 deploy success; report both.
