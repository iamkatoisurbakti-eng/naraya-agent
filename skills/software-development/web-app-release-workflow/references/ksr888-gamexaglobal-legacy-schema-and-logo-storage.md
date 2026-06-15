# KSR888 GameXaGlobal legacy schema + logo storage notes

Scope
- Imported PHP/Laravel host `ksr888.online` served by `ksr888-web` from `/root/nusantara-ai-saas/KSR888/site`.
- Applies when enabling live GameXaGlobal sync and fixing logo/icon paths across public/admin surfaces.

## Root causes found
- KSR888 has two branding sources:
  - legacy PHP pages use `tb_web.logo` / `tb_web.icon_web` and serve files from `/assets/img/<file>`.
  - Laravel Blade/public/admin routes use `genral_settings.logo` / `genral_settings.favicon` and serve files from `/storage/<file>`.
- Updating only `tb_web` leaves Laravel-rendered pages pointing at stale `/storage/0`.
- GameXaGlobal sync code assumed modern timestamped tables, but the live legacy tables have no `created_at` / `updated_at` columns.
- The live `providers` table has required non-null columns with no defaults: `slug`, `jenis`, `providerapi`.
- The live `games` table requires `g_type` and `game_api`, and `status` is an integer; upstream values such as `active` must be normalized to `1`.

## Fix pattern
1. Probe live schema before sync changes:
   ```bash
   docker exec ksr888-web php -r '$pdo=new PDO("mysql:host=".getenv("DB_HOST").";port=".getenv("DB_PORT").";dbname=".getenv("DB_NAME"),getenv("DB_USER"),getenv("DB_PASSWORD")); foreach(["providers","games","api","genral_settings","tb_web"] as $t){ echo "$t\n"; foreach($pdo->query("SHOW COLUMNS FROM `$t`") as $r){ echo "  {$r["Field"]}\n"; }}'
   ```
2. In provider upserts:
   - add `slug = strtolower(provider_code)` when column exists
   - add `jenis = 1` when column exists
   - add `providerapi = gamexaglobal` when column exists
   - only add `created_at` / `updated_at` if `Schema::hasColumn(...)` returns true
3. In game upserts:
   - normalize upstream `status` strings (`active`, `enabled`, `1`) to integer `1`; otherwise `0`
   - add `g_type = game_type` when column exists
   - add `game_api = gamexaglobal` when column exists
   - only add timestamp fields when columns exist
4. For logo/icon fixes, copy the same valid logo into both places:
   - `KSR888/site/assets/img/<logo>.png`
   - `KSR888/site/public/storage/<logo>.png`
   - `KSR888/site/backoffice/assets/img/<logo>.png`
5. Update both DB rows:
   - `tb_web.logo`, `tb_web.icon_web`
   - `genral_settings.logo`, `genral_settings.favicon`
6. Rebuild/recreate `ksr888-web` with production env loaded, restart Caddy, and clear Laravel cache.

## Verification checklist
- `docker exec ... php -l app/Http/Controllers/GameController.php`
- GameXaGlobal probes from container:
  - `me ok status=200`
  - `providers ok status=200`
  - `games ok status=200`
- DB counts should increase/populate:
  - `providers`
  - `games`
  - `gamexaglobal_snapshots`
  - `api.gx_last_sync_at`
- HTTP smoke with browser UA:
  - `/` renders logo from `/storage/<logo>.png`
  - `/support` and `/admin` render logo from `/storage/<logo>.png`
  - `/assets/img/<logo>.png` returns 200 image/png
  - `/storage/<logo>.png` returns 200 image/png
  - `/slots`, `/casino`, `/fishing`, `/hot` return 200 and contain provider/game terms

## Pitfalls
- `vendor/bin/phpunit` may be absent inside the PHP image; use PHP lint + HTTP/DB/API smoke as the release gate.
- Partial sync failures can leave providers inserted but games unchanged. Tail `storage/logs/laravel.log` and look for schema errors before retrying.
- Do not print GameXaGlobal tokens or credentials. Report only masked configured/missing or status codes.
