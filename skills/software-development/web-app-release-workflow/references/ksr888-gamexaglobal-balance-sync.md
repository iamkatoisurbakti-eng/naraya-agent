# KSR888 GameXaGlobal automatic balance sync

Use when fixing KSR888 user wallet balance drift between local `saldo` and GameXaGlobal provider balances.

## Context
- Repo: `/root/nusantara-ai-saas/KSR888/site`
- Live container: `nusantara-ai-saas-ksr888-web-1`
- App path in container: `/var/www/html`
- Public site: `https://ksr888.online`
- Runtime often lacks host `php`; run PHP/Laravel checks inside Docker.

## Proven fix pattern
1. Create/maintain a class-level service rather than duplicating balance sync code in controllers:
   - `app/Services/GameXaGlobalBalanceSyncService.php`
   - Use `App\Http\Api\gamexaglobal`.
   - Resolve provider username from `User.extplayer ?: User.name`, lowercased.
   - Find provider player via `$gx->players(['search' => $username, 'page' => 1, 'limit' => 30])`.
   - Extract player id from `id`, `player_id`, or `user_id`.
   - Fetch balance via `$gx->playerBalance($playerId)`.
   - Update local `Saldo::updateOrCreate(['user_id' => $user->id], ['user_name' => $user->name, 'saldo' => $balance])`.
2. Wire user-facing auto sync through `HomeController@saldoRefresh`:
   - Inject the sync service.
   - If unauthenticated return JSON-ish error with 401.
   - `firstOrCreate` local saldo for the logged-in user.
   - Try provider sync with `createIfMissing=true`.
   - Return the existing text/plain JSON contract used by current Blade JS: `{error:false,balance:<number>,provider:'gamexaglobal'}`.
   - On provider failure, fall back to local balance instead of breaking page UX.
3. Wire admin bulk refresh through `GetSaldoController@saldo`:
   - Inject the same sync service.
   - Rate-limit via cache key such as `ksr888:saldosync:last_run`.
   - Iterate non-admin users in batches/limits.
   - Return a concise Indonesian summary: total/sync/gagal.
4. Use cache/locks in the service to avoid refresh-button spam:
   - Per-user lock key like `ksr888:gx-balance-sync:{user_id}:lock`.
   - Short cache for last balance (e.g. 20s last run, 2m balance).

## Deploy and verification
- Copy changed files into the running container when using this KSR888 deployment pattern:
  - `docker cp <file> nusantara-ai-saas-ksr888-web-1:/var/www/html/<file>`
- Syntax check in container:
  - `docker exec nusantara-ai-saas-ksr888-web-1 sh -lc 'cd /var/www/html && php -l app/Services/GameXaGlobalBalanceSyncService.php && php -l app/Http/Controllers/HomeController.php && php -l app/Http/Controllers/GetSaldoController.php'`
- Clear Laravel caches with a PTY via compose; raw `docker exec` can fail with `StreamOutput class needs a stream`:
  - `cd /root/nusantara-ai-saas && docker compose exec ksr888-web sh -lc 'cd /var/www/html && php artisan optimize:clear --no-ansi'`
- Restart after deploy:
  - `cd /root/nusantara-ai-saas && docker compose restart ksr888-web`
- Verify routes:
  - `docker compose exec ksr888-web sh -lc 'cd /var/www/html && php artisan route:list --path=saldo-refresh --no-ansi && php artisan route:list --path=update/saldo --no-ansi'`
- Verify service without exposing secrets by running a temporary local script in `/var/www/html/tmp/` that boots Laravel, selects a non-admin user, calls `GameXaGlobalBalanceSyncService::syncUser($user, false)`, and prints only `ok/message/has_balance`.
- Verify public live site:
  - `curl -I -L --max-time 15 https://ksr888.online/ | head -20`

## Pitfalls
- Do not use the old BGX + Softgaming combined balance logic for current KSR888 GameXaGlobal wallet sync.
- Do not echo provider tokens/API keys in logs or final replies.
- Do not leave temporary verification scripts in the repo/container after testing.
- Keep the frontend response shape compatible with existing jQuery that calls `JSON.parse(data)` on `/saldo-refresh`.
