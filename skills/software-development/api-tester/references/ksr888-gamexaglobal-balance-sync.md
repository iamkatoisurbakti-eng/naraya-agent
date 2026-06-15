# KSR888 GameXaGlobal balance sync API verification

Use when validating KSR888 automatic wallet sync against GameXaGlobal.

## Endpoint/contracts
- User-facing refresh: `GET /saldo-refresh` (auth required)
  - Existing Blade JS expects text/plain body parseable by `JSON.parse(data)`.
  - Success shape: `{error:false,balance:<number>,provider:'gamexaglobal'|'local',cached?:bool}`.
  - Unauth shape: `{error:true,message:'Unauthenticated',balance:0}` with 401.
- Admin bulk refresh: `GET /update/saldo` inside admin middleware.
  - Returns Indonesian text summary with total/synced/failed.

## Provider verification
- Do not print real GameXaGlobal credentials/tokens.
- Prefer a temporary Laravel bootstrap script in `/var/www/html/tmp/` that calls `App\Services\GameXaGlobalBalanceSyncService::syncUser($user, false)` and prints only:
  - `user_id`
  - `ok`
  - `message`
  - `has_balance`
  - `cached`
- Delete the temporary script from source and container after testing.

## Docker/Laravel commands
- Host may not have `php`; use the KSR888 container.
- Syntax check:
  `docker exec nusantara-ai-saas-ksr888-web-1 sh -lc 'cd /var/www/html && php -l app/Services/GameXaGlobalBalanceSyncService.php && php -l app/Http/Controllers/HomeController.php && php -l app/Http/Controllers/GetSaldoController.php'`
- Route check needs PTY via compose if Artisan console output fails under raw docker exec:
  `cd /root/nusantara-ai-saas && docker compose exec ksr888-web sh -lc 'cd /var/www/html && php artisan route:list --path=saldo-refresh --no-ansi && php artisan route:list --path=update/saldo --no-ansi'`

## Pitfall
- Old KSR888 code combined BGX and Softgaming balances. For current GameXaGlobal wallet sync, validate `gamexaglobal->players()` + `playerBalance()` and local `saldo` update instead.
