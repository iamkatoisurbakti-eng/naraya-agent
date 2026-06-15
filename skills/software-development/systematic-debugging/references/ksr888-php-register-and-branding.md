# KSR888 PHP register redirect + branding cache notes

## Register redirect symptom
If a user clicks **Daftar** and lands back on home, check the actual form handler, not only the view:
- Legacy mobile: `KSR888/site/mobile/function/daftar_akun.php`
- Legacy desktop: `KSR888/site/dekstop/function/daftar_akun.php`
- Laravel register: `KSR888/site/app/Http/Controllers/Auth/RegisterController.php`

In this repo, a successful create can still appear to "fail" if the redirect goes to a profile/home URL that does not surface success. For the current KSR888 production flow, successful registration should log the user in and redirect directly to the game lobby / provider listing, e.g.:
- Legacy mobile/desktop: `../index.php?page=slot`
- Laravel: `/slots/server-b/5g/SL`

## Register API/database sync pitfall
KSR888 has two user surfaces that must stay in sync:
- Laravel tables: `users`, `saldos`/`saldo` model backing table
- Legacy PHP tables: `tb_user`, `tb_saldo`, `tb_bank`

When changing registration, patch both flows, not just one:
1. Legacy handlers (`mobile/function/daftar_akun.php`, `dekstop/function/daftar_akun.php`) should insert legacy rows and also sync a Laravel `users` row.
2. Laravel `RegisterController::create()` should create the Laravel user and also `updateOrInsert` matching legacy `tb_user`, `tb_saldo`, and `tb_bank` rows.
3. Registration should create/sync the real production GameXaGlobal player before declaring success, using `POST /api/players` with the complete payload required by the provider: `agent_code`, `player_id`, `user_id`, `user_code`, `username`, `player_name`, `full_name`, `name`, `email`, `password`, `phone`, `currency`, `language`, `status`.
4. If `POST /api/players` fails because the player already exists, verify via `GET /api/players?search=<extplayer>` before failing registration.
5. Use `GET /api/players/{id}/balance` only after resolving the numeric provider player id from `GET /api/players`; do not assume local `extplayer` is the provider id.
6. Never print API tokens, agent codes, or DB credentials in logs or final replies; report `[SET]`/`[REDACTED]` only.

## Branding/logo not changing
If the logo looks unchanged after deploy:
1. Verify the runtime DB values, not just the source tree:
   - `tb_web.logo`
   - `tb_web.icon_web`
2. Copy the new asset into every path the app serves from:
   - `assets/img/`
   - `mobile/assets/img/`
   - `backoffice/assets/img/`
   - `public/assets/img/`
3. Use a new filename or query-busted path so the browser doesn't keep the old image.
4. Verify the *served* file hash inside the container, not only the host copy.

## Verification commands
- Read the live DB row from inside the container.
- `grep` the PHP handlers for the redirect target.
- `curl` the live page and confirm the expected `logo` filename appears.
- `sha256sum` the served asset in-container and compare with the source image.
