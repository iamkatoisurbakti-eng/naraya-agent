# KSR888 production evaluation + launch audit notes

Use when evaluating or fixing `ksr888.online` production readiness after GameXaGlobal/provider/image changes.

## Fast evidence checklist
- Use browser-like UA for live pages; plain curl can return misleading/minimal responses.
- Verify containers and logs first:
  - `docker compose ps --format 'table {{.Name}}\t{{.Service}}\t{{.Status}}'`
  - `docker compose exec -T ksr888-web sh -lc 'tail -n 120 storage/logs/laravel.log 2>/dev/null || true'`
  - `docker compose logs --tail=250 ksr888-web 2>&1 | grep -Ei 'fatal|exception|error|warning|AH00558|SQLSTATE|Invalid token' | tail -n 80 || true`
- Run container-side lint/tests because host PHP may be missing:
  - `docker compose exec -T ksr888-web sh -lc 'php -l app/Http/Controllers/GameController.php && php -l app/Http/Api/gamexaglobal.php && php ./vendor/bin/phpunit --filter GameControllerProviderImageSyncTest'`

## Launch-game root cause pattern
- KSR888 live catalog can be healthy while game launch is blocked by upstream auth.
- If GameXaGlobal probes return `403 Invalid token` for `/api/auth/me`, `/api/games/providers`, or `/api/games`, do not keep patching UI/DB launch code as the primary fix.
- Report the blocker as: wiring/catalog/fallback OK, upstream launch/sync blocked until a valid GameXaGlobal token/credential is installed.
- Keep token output masked; never echo `gx_token`, `GAME_LIBRARY_TOKEN`, or connection strings.

## Image completeness pattern
- For production image coverage, audit DB counts directly:
  - active providers with `provider_image`, `banner`, `mobile_banner`
  - active games with `game_image`
- Backfill provider blanks from available sibling fields (`provider_image`, `banner`, `mobile_banner`) and game blanks from matching provider image/banner. If a final active game has no provider match, use a safe same-origin placeholder such as `/assets/img/logo.png` or full `https://ksr888.online/assets/img/logo.png`.
- Rendered frontend should keep raw remote image URLs in DB and serve remote images through `/game-image-proxy` via model accessors/templates.

## Live asset audit pitfall
- Audit rendered HTML assets by extracting `src`, `href`, and `data-src`, then probe image-like URLs directly.
- A common non-game broken asset is favicon/icon `https://ksr888.online/storage/0`. Treat this as a P1 polish/security-quality issue, not a provider/game image coverage failure.

## Production scoring heuristic
- Consider public frontend healthy when key routes return 200 with browser UA, logs are clean, PHP tests pass, and provider/game image coverage is 100%.
- Keep a P0 blocker if real launch upstream still returns `403 Invalid token`, even when catalog pages are healthy.
