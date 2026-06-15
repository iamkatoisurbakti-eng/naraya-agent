# KSR888 Game launch troubleshooting

Use this note when fixing GameXaGlobal game launch issues in `/root/nusantara-ai-saas/KSR888/site`.

## What launch should send
For `POST /api/games/launch`, the launch helper should prefer the documented payload shape:
- `player_id`
- `game_uid`
- `lobby_url`
- `lang`

Useful fallback aliases can be tried only if the provider rejects the primary payload, but the documented fields should be the first attempt.

## URL handling
- Preserve the launch URL returned by GameXaGlobal exactly as received.
- Do not rewrite `api.httpsgamexaglobal.net` to another host unless the upstream contract explicitly changes.
- If the returned object contains `game_launch_url`, `launch_url`, `gameUrl`, or `url`, use the first valid absolute URL.

## Lobby URL construction
- When the code needs a local lobby/return URL, prefer a test-safe fallback that uses, in order:
  - `FRONTEND_URL`
  - `APP_URL`
  - `APP_PUBLIC_URL`
- If none are available, fall back to a relative path instead of hard-failing on Laravel's `url()` helper.

## Verification pattern
1. Lint the changed PHP files inside the container.
2. Run the focused PHPUnit class that exercises launch payloads and URL extraction.
3. Rebuild/recreate the `ksr888-web` container if the live site is served from Docker.

Example checks:
- `docker compose exec -T ksr888-web sh -lc 'php -l /var/www/html/app/Http/Controllers/GameController.php'`
- `docker compose exec -T ksr888-web sh -lc 'php vendor/bin/phpunit --filter GameControllerProviderImageSyncTest --testdox'`
- `docker compose build ksr888-web && docker compose up -d --no-deps --force-recreate ksr888-web`

## Common failure modes
- Launch succeeds in API docs but the app still redirects home because the returned launch URL was rewritten or discarded.
- Tests fail because a helper calls `url()` in a non-HTTP context.
- Payload retries keep failing because the game identifier field was sent as the wrong name.
