# KSR888 GameXaGlobal slot launch + provider UI notes

Use when KSR888 slot cards click but do not open a game, or when provider cards show unwanted CTA buttons.

## Observed root cause
- Frontend slot cards may still emit legacy provider/game IDs, for example provider `PR` and game codes like `vs20olympgold` or `vswayslions`.
- GameXaGlobal live launch requires upstream provider codes and upstream game codes, for example `PRAGMATIPLAY_SLOT` plus hash-like game codes from `/api/games` or `/api/games/provider/{providerCode}`.
- Direct launch with old code can return `404 Game not found or inactive` even though the local DB game exists.
- The local KSR888 `games` table in this environment has `game_type` but not `game_category`; check schema before querying both columns.

## Fix pattern
1. Trace click path:
   - Provider page: `resources/views/slots/provider.blade.php` and `resources/views/slots/other.blade.php`.
   - Game list: `resources/views/slots/games.blade.php` / `server-b.blade.php`.
   - Launch route: `/game_process/{game_code}/{game_provider}` -> `GameController::connect_games`.
2. In `GameController`, before `launchGame()`, resolve legacy local provider/game into GameXaGlobal values:
   - Map provider aliases such as `PR` -> `PRAGMATIPLAY_SLOT` (and `PRAGMATIC_LIVE_ASIA` for live casino).
   - Fetch/cache active upstream catalog with `/api/games` (large limit if supported).
   - Match by exact upstream code first, then normalized game name (strip symbols like ™/®, non-alphanumeric, lowercase).
   - Replace provider_code/game_code in the launch payload with upstream values.
3. Verify with a logged-in test user by directly invoking the controller or live route and confirm:
   - HTTP status is 302.
   - `Location` is an external launch URL (host observed: `api.gamexaglobal.com`).
   - Logs do not contain `Game launch rejected`, `GameXaGlobal launch rejected`, `PHP Fatal`, or parse errors.

## Provider page button removal pattern
When the user asks to remove all buttons on provider game cards:
- Remove desktop `.btn-wrapper` / `.btn-hvrplay` markup and its forced-visible CSS from `slots/provider.blade.php` and `slots/other.blade.php`.
- Remove mobile `.provider-play-now-btn` spans and CSS.
- Keep the surrounding `<a href="{{ $provider->detail_url }}" class="game">` card link so provider cards remain clickable.
- Verify live `/slots` HTML no longer contains `btn-hvrplay`, `provider-play-now-btn`, or `MAIN SEKARANG`, while `games-category` and provider card links still exist.

## Container/deploy notes
- Host PHP may be unavailable; use `docker exec nusantara-ai-saas-ksr888-web-1 php -l ...` for linting.
- Rebuild/recreate KSR888 web after source changes: `docker compose build ksr888-web && docker compose up -d --force-recreate ksr888-web` from `/root/nusantara-ai-saas`.
- Clear cache via live `/clear-cache` when artisan has TTY/StreamOutput problems.
- Avoid echoing secrets/tokens in output.