---
name: ksr888-gamexaglobal-dedup-and-admin-transactions
summary: Session notes for KSR888 GameXaGlobal duplicate provider/game cleanup plus admin transactions-overview wiring.
---

# KSR888 GameXaGlobal dedup + admin transactions notes

## Trigger
Use when KSR888 provider/game catalog looks duplicated, admin Game Library shows repeated providers/games, or `/transactions-overview` needs live GameXaGlobal transaction/turnover data.

## Root causes found
- `providers` is a legacy table with no `created_at` / `updated_at`; insert rows also require `slug`, `jenis`, and `providerapi`.
- `games` is a legacy table with no `created_at` / `updated_at`; insert rows also require `g_type`, `game_api`, and integer `status`.
- Provider sync must treat `provider_code + provider_type` as the identity. Looking up existing providers by `provider_code` alone can mix images/metadata across category variants.
- Runtime provider map should keep both `provider_code:provider_type` and a first-seen `provider_code` fallback; the provider-specific fetch loop must iterate only unique provider codes, not every provider map key.
- Exact duplicates can survive previous failed sync attempts and must be cleaned after a corrected sync.
- `/transactions-overview` should not call the old `fiver()` history flow after GameXaGlobal becomes the active provider.

## Fix pattern
1. Patch `app/Http/Controllers/GameController.php` sync logic:
   - compute `providerType` before existing-row lookup
   - lookup `providers` by both `provider_code` and `provider_type`
   - only set timestamp fields when `Schema::hasColumn(...)`
   - set legacy-required fields when present: `slug`, `jenis`, `providerapi`, `g_type`, `game_api`
   - normalize GameXa `status: active` to DB integer `1`
2. Store provider map as:
   - `$providerRows[$providerCode . ':' . $providerType] = $providerRecord`
   - `$providerRows[$providerCode]` only as fallback if absent
3. Iterate provider game detail sync with unique provider codes:
   - `array_values(array_unique(array_map(fn ($key) => explode(':', (string) $key)[0], array_keys($providerRows))))`
4. After sync, remove exact duplicates:
   ```sql
   DELETE p1 FROM providers p1
   INNER JOIN providers p2
     ON p1.provider_code = p2.provider_code
    AND p1.provider_type = p2.provider_type
    AND p1.id > p2.id;

   DELETE g1 FROM games g1
   INNER JOIN games g2
     ON g1.game_provider = g2.game_provider
    AND g1.game_code = g2.game_code
    AND g1.id > g2.id;
   ```
5. For `/transactions-overview`, patch `GameSettingController` to use `App\\Http\\Api\\gamexaglobal`:
   - populate player select from `/api/players`
   - add a `__all__` / `Semua Player — Transaction Management` option for global transaction mode
   - for selected player mode, fetch row history from `/api/players/{playerId}/transactions`
   - for all-player Transaction Management mode, fetch row history from `/api/transactions`
   - fetch summary metrics from `/api/transactions/stats` and prefer those values for dashboard cards when present
   - fetch turnover rows from `/api/transactions/turnover-by-player`
   - if turnover is empty, render a summary fallback row so the UI still proves the flow works.
6. If the user asks to “sambungkan Transactions”, add the cleaner admin alias while preserving backward compatibility:
   - `GET /transactions` -> `GameSettingController@showForm`, named `transactions`
   - `POST /transactions/search` -> `GameSettingController@getGameHistory`, named `transactions.search`
   - keep `/transactions-overview` and `/transactions-overview/search` active as aliases for old bookmarks
   - point sidebar/menu links to `/transactions`, but keep active-state checks for both `/transactions` and `/transactions-overview`
   - in `history.blade.php`, set the AJAX `searchUrl` to `route('transactions.search')`
   - add a `Buka Transactions` button from Game Library's Transactions panel to `/transactions` so the endpoint status panel connects to the live management screen.
7. Update the admin view/menu together:
   - use the user-facing label `Transactions` when the user asks for that menu name; otherwise `Transaction Management` is acceptable for the detailed page
   - include columns for player, amount, status, and time in the transaction table and CSV export
   - update DataTables sort index after adding columns (time column moved to index 9 in this session)
   - keep the page route stable at `/transactions-overview` so existing admin links/bookmarks still work even after `/transactions` becomes the primary URL.

## Verification commands
Run inside the repo root after deploy/restart. Prefer container `php -r` or small temporary raw-PHP probes for GameXa transaction checks; this host can throw Symfony `StreamOutput` errors when bootstrapping Laravel from a non-interactive copied script.

```bash
docker exec -w /var/www/html nusantara-ai-saas-ksr888-web-1 php -l app/Http/Controllers/GameController.php

docker exec nusantara-ai-saas-ksr888-web-1 php -r '\
$db=new mysqli(getenv("DB_HOST"),getenv("DB_USER"),getenv("DB_PASSWORD"),getenv("DB_NAME"),(int)getenv("DB_PORT")); \
$r=$db->query("SELECT gx_token,gx_endpoint FROM api LIMIT 1")->fetch_assoc(); \
$endpoint=rtrim($r["gx_endpoint"],"/"); $token=$r["gx_token"]; \
foreach(["/api/auth/me","/api/transactions","/api/transactions/stats","/api/transactions/turnover-by-player"] as $path){ \
  $ch=curl_init($endpoint.$path); \
  curl_setopt_array($ch,[CURLOPT_RETURNTRANSFER=>true,CURLOPT_TIMEOUT=>20,CURLOPT_HTTPHEADER=>["Accept: application/json","Authorization: Bearer ".$token]]); \
  curl_exec($ch); echo $path."=".curl_getinfo($ch,CURLINFO_RESPONSE_CODE)."\\n"; curl_close($ch); \
}'

docker exec nusantara-ai-saas-ksr888-web-1 php -r '\
$pdo=new PDO("mysql:host=".getenv("DB_HOST").";port=".getenv("DB_PORT").";dbname=".getenv("DB_NAME").";charset=utf8mb4",getenv("DB_USER"),getenv("DB_PASSWORD")); \
$pd=$pdo->query("SELECT COUNT(*) c FROM (SELECT provider_code,provider_type FROM providers GROUP BY provider_code,provider_type HAVING COUNT(*)>1) x")->fetch(PDO::FETCH_ASSOC)["c"]; \
$gd=$pdo->query("SELECT COUNT(*) c FROM (SELECT game_provider,game_code FROM games GROUP BY game_provider,game_code HAVING COUNT(*)>1) x")->fetch(PDO::FETCH_ASSOC)["c"]; \
echo "provider_duplicate_groups=$pd\\n"; \
echo "game_duplicate_groups=$gd\\n"; \
'
```

Expected live result from this session:
- `providers=144`
- `games=11467`
- `provider_duplicate_groups=0`
- `game_duplicate_groups=0`
- GameXa `me/providers/games` all `ok status=200`
- Transaction Management probes return `200` for `/api/auth/me`, `/api/transactions`, `/api/transactions/stats`, and `/api/transactions/turnover-by-player`; empty arrays are acceptable when no transactions exist for the selected date.
- routes `/`, `/slots`, `/casino`, `/sports`, `/p2p`, `/fishing`, `/lottery`, `/hot`, `/support`, and `/transactions-overview` return HTTP 200
- `storage/logs/laravel.log` stays clean after smoke.

## Pitfalls
- Do not create a database unique index on these legacy tables without first checking column types; `provider_code` and `slug` are `text` in this import, so index creation may fail or require prefix lengths.
- `php artisan optimize:clear` can intermittently fail with `StreamOutput` when chained after `docker compose restart`; retry it as a separate `docker exec` command.
- `php artisan route:list` can fail because unrelated stale routes reference missing classes; do not use it as the main verification gate for this host.
- Do not print GameXa tokens or agent credentials during probes; use ok/status-only output.
- When probing GameXa transaction endpoints, a `200` with empty `transactions` / `players` arrays means the integration is reachable but there is no data for that date range; do not treat it as a failed connection.
- For `/transactions-overview`, a 200 response may be the login redirect shell if unauthenticated. Verify the deployed code by grepping the container files for `Transaction Management`, `__all__`, and `$gx->transactions(...)`, then do browser/session auth only if you need to test hydrated admin behavior.
