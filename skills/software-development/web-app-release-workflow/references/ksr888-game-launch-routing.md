# KSR888 game launch routing and deploy checklist

Use when KSR888 provider/category pages load but clicking providers/games cannot launch games, redirects unexpectedly, or nested pages break assets.

## Symptoms seen
- `/slots` rendered provider cards, but provider links like `/slots/server-a/{provider}` returned 404 or bounced back.
- Game cards used mismatched launch URLs, e.g. `/game_process2/{game_code}` while the route expected model binding by `{game:id}`.
- Guest links used `/game_process/{id}` even though the launch route requires `/game_process/{game_code}/{game_provider}`.
- Nested URLs such as `/slots/server-b/pg/SL` caused relative assets like `assets/images/log_html5.png` to resolve under the nested path.
- Legacy provider API env/table values were empty while GameXaGlobal config was present, so launch should fall back to GameXaGlobal rather than only old providers.

## Proven fix pattern
1. Inspect live logs first; route misses show up as 404s for provider pages and wrong launch endpoints.
2. Add explicit authenticated routes for provider detail pages:
   - `/slots/server-a/{provider_code}`
   - `/slots/server-b/{provider_code}/{provider_type}`
   - category aliases like `/{category}/server-a/...` and `/{category}/server-b/...` with a whitelist.
3. Make provider `detail_url` point to the real provider game list route, usually `/{category}/server-b/{provider}/{type}`, not back to category landing pages.
4. Standardize play buttons to `/game_process/{game_code}/{game_provider}` for logged-in users; guests should go to `/masuk` or trigger login, not malformed launch URLs.
5. In `connect_games`, if a legacy launch fails or legacy config is empty, try `launchGameXaGlobal()` before returning an error.
6. Add `<base href="{{ url('/') }}/">` in the desktop and mobile main layout heads so nested provider URLs do not break relative static assets.
7. Rebuild and recreate `ksr888-web`; source edits do not affect the running container until the image is rebuilt.

## Verification commands
```bash
cd /root/nusantara-ai-saas

docker compose build ksr888-web
# Run detached as background if the tool classifies compose up as long-lived
docker compose up --no-build -d ksr888-web

docker compose exec -T ksr888-web bash -lc \
  'php -l app/Http/Controllers/GameController.php && php -l app/Models/SgProvider.php && php -l routes/web.php'

curl -A 'Mozilla/5.0' -s https://ksr888.online/slots -o /tmp/ksr_slots.html
python3 - <<'PY'
import re
html=open('/tmp/ksr_slots.html',encoding='utf-8',errors='ignore').read()
print('/slots/server-b/' in html)
print('/slots/server-a/' in html)
print(bool(re.search(r'/game_process/\d+["\']', html)))
print('<base href="https://ksr888.online/">' in html)
PY
```

Expected:
- `/slots/server-b/` present in provider links.
- No stale `/slots/server-a/` provider links from `/slots` unless intentionally supported.
- No one-argument `/game_process/{id}` launch links.
- Base tag present in live HTML.

## Pitfalls
- Do not query `sg_providers`; this KSR888 model uses the legacy `providers` table.
- The `api` table is singular, not `apis`.
- `php` may not exist on the host; run syntax checks inside `ksr888-web`.
- `php artisan route:list` can fail because unrelated legacy controllers are missing; prefer HTTP smoke tests and direct `php -l` for changed files.
- Public curl of authenticated provider detail pages can 302 to home/login; verify rendered links from public category pages and use browser/auth smoke for actual launch.
- Some terminal wrappers classify `docker compose up -d` as long-lived; run it as a background process and then wait/check readiness.
