# KSR888 Provider → Game List → Launch Flow

Session learning from KSR888 Laravel/PHP site (`/root/nusantara-ai-saas/KSR888/site`). Use when adjusting provider cards, game lists, or GameXaGlobal launch behavior.

## Intended UX
1. Category page (`/slots`, `/casino`, etc.) shows provider cards.
2. Clicking a provider must open that provider's game list, not auto-launch a game.
   - Expected URL shape: `/{category}/server-b/{provider_code}/{provider_type}`.
   - Example: `/slots/server-b/PR/SL`.
3. Clicking an actual game card launches that game.
   - Expected URL shape: `/game_process/{game_code}/{game_provider}`.
4. If the user is not logged in, game click should route to `/masuk` rather than attempting launch.

## Files involved
- `app/Models/SgProvider.php`
  - `getDetailUrlAttribute()` controls provider-card target URLs.
  - Map provider type to category and return `url('/' . $category . '/server-b/' . $provider . '/' . $type)`.
- `routes/web.php`
  - Existing routes include `/{category}/server-b/{provider_code}/{provider_type}` → `GameController@slotShow` and `/game_process/{game_code}/{game_provider}` → `GameController@connect_games`.
  - Keep `/provider-launch` only as compatibility if needed; do not use it from provider cards for this UX.
- `app/Http/Controllers/GameController.php`
  - `slotShow()` loads provider-specific active games.
  - `connect_games()` launches via the configured game API/GameXaGlobal.
- `resources/views/slots/games.blade.php`
  - Authenticated game cards/buttons should point to `/game_process/...`.
  - Guest game cards/buttons should point to `/masuk`.
- `resources/views/slots/other.blade.php` and `resources/views/slots/provider.blade.php`
  - Provider anchors should use `$provider->detail_url` without `target="_blank"`; the user's preferred provider click behavior is same-tab navigation into the provider game list first, not a pop-up/new tab and not auto-launch.
- `resources/views/slots/server-b.blade.php`
  - This is another provider-specific game-list template. If edits to `slots/games.blade.php` do not affect live provider pages, inspect and patch this file too.

## Verification checklist
Run syntax checks inside the container, because host PHP may be missing:

```sh
docker exec nusantara-ai-saas-ksr888-web-1 sh -lc 'cd /var/www/html && php -l app/Models/SgProvider.php && php -l resources/views/slots/games.blade.php && php -l routes/web.php && php -l app/Http/Controllers/GameController.php'
```

Rebuild/restart from repo root:

```sh
cd /root/nusantara-ai-saas
docker compose build ksr888-web
docker compose up -d ksr888-web
curl -k -sS https://ksr888.online/clear-cache
```

Probe live pages:

```sh
python3 - <<'PY'
import requests,re,urllib3
urllib3.disable_warnings()
base='https://ksr888.online'
slots=requests.get(base+'/slots?cb=verify',timeout=25,verify=False).text
print('provider server-b links', len(re.findall(r'href="([^"]*/slots/server-b/[^"]+)"', slots)))
print('provider-launch links', slots.count('/provider-launch/'))
for path in ['/slots/server-b/PR/SL','/slots/server-b/hacksaw/SL']:
    body=requests.get(base+path+'?cb=verify',timeout=25,verify=False).text
    print(path, 'game-boxes', body.count('game-box'), 'guest /masuk links', body.count('/masuk'), 'game_process refs', body.count('/game_process/'))
PY
```

For unauthenticated probes, game list pages should usually show `/masuk` rather than `/game_process/`; verify source templates for authenticated `/game_process/` links if no test login is available.

## Pitfalls
- A previous implementation changed provider cards to `/provider-launch/...`, which auto-launched a preferred/first game. Revert that for the requested provider → choose game → launch flow.
- `docker compose up -d ...` may be flagged as long-lived by the agent shell; run it as a background process if necessary, then wait/check logs.
- `php artisan optimize:clear` can fail in this container with `StreamOutput class needs a stream`; the live `/clear-cache` route has worked as a fallback.
- `git -C /root/nusantara-ai-saas status` may fail if the deployment directory is not a Git checkout; do not rely on Git for verification there.
