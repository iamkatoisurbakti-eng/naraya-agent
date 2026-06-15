# KSR888 GameXaGlobal Player Management

Session learning from KSR888 `/players` admin work.

## Scope
Use this when adding or verifying admin-side player management for KSR888 with GameXaGlobal.

## Working pattern
1. Keep provider credentials in env/DB config only; never print tokens.
2. Use `App\Http\Api\gamexaglobal`, not legacy `bgx`/hardcoded providers, for live provider actions.
3. For provider listing, call:
   - `GET /api/players` via `$gx->players(['page' => 1, 'limit' => N, 'search' => $term])`
4. Normalize player rows defensively. Observed possible fields:
   - id: `id`, `player_id`, `user_id`, fallback username
   - username: `username`, `user_code`, `player`, `name`
   - balance: `balance`, `wallet.balance`
   - status: `status`, `is_active`
5. Map local users by lowercase `extplayer ?: name` to provider username.
6. Safe local actions:
   - Sync balance: resolve exact provider username first, then call `$gx->playerBalance($providerId)`, then `Saldo::updateOrCreate(['user_id' => ...], ['user_name' => ..., 'saldo' => ...])`.
   - Player create must be idempotent and single-source: one local user maps to exactly one GameXaGlobal player that can access all providers. Never create per-provider players, never mass-create during balance sync, and do not call legacy BGX/Softgaming create paths.
   - Centralize resolve/create in a service (e.g. `GameXaGlobalPlayerService`) that first searches exact username (`extplayer ?: name`), then creates via `$gx->createPlayer()` only if missing, treats duplicate/already-exists as success by resolving again, and uses a per-username cache lock to avoid simultaneous duplicate creates.
   - Bulk/admin balance sync should use resolve-only (`createIfMissing=false`) to avoid accidental mass provider account creation.

## Launch/deposit/withdraw integration rule
When launch, deposit, withdraw, QRIS callback, admin deposit approval, registration, or admin member creation needs a provider player, call the same idempotent GameXaGlobal player service. Do not duplicate `ensureGamexaglobalPlayerId()` implementations across controllers unless they delegate to that service. This prevents drift where one flow creates `name`, another creates `extplayer`, and another creates provider-specific duplicates.

## Routes/UI pattern used
Admin routes added under authenticated admin group:
- `GET /players` -> `DatamemberController@players`
- `POST /players/{id}/sync-balance` -> `syncPlayerBalance`
- `POST /players/{id}/create-provider` -> `createProviderPlayer`

Add sidebar entry under Member menu, and keep `/players` protected by admin auth. Public curl should return a login redirect, not page content.

## Verification
Run inside the container after rebuild/recreate:

```bash
docker exec nusantara-ai-saas-ksr888-web-1 php -l app/Http/Controllers/backoffice/DatamemberController.php
docker exec nusantara-ai-saas-ksr888-web-1 php -l routes/web.php
docker exec nusantara-ai-saas-ksr888-web-1 php -l resources/views/admin/players/management.blade.php
```

Probe the provider without printing secrets:

```php
$gx = new App\Http\Api\gamexaglobal();
$response = $gx->players(['page' => 1, 'limit' => 3]);
echo 'gx_configured=' . ($gx->configured() ? '1' : '0') . PHP_EOL;
echo 'gx_status=' . (int)($response['status'] ?? 0) . PHP_EOL;
echo 'gx_ok=' . (($response['ok'] ?? false) ? '1' : '0') . PHP_EOL;
```

Expected healthy result: configured `1`, status `200`, ok `1`.

## Pitfalls
- Local CLI `php` may not exist on host; run PHP checks inside `nusantara-ai-saas-ksr888-web-1`.
- `php artisan optimize:clear` inside this container may fail with `StreamOutput class needs a stream as its first argument` when there is no TTY. Prefer `docker compose exec ksr888-web ...` with PTY (or terminal tool `pty=true`); if unavailable, use the app `/clear-cache` route fallback and verify `DONE`.
- If host paths differ, check the live repo root first. In some sessions KSR888 source is under `/root/nusantara-agent/nusantara-ai-saas/KSR888/site`, while older notes may mention `/root/nusantara-ai-saas/KSR888/site`.
- `/players` should 302 redirect when unauthenticated; render verification can be done by bootstrapping Laravel in-container with a synthetic request and admin login.
