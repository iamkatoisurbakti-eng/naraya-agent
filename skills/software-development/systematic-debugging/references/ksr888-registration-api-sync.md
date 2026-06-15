# KSR888 registration API sync + redirect pitfalls

Use when KSR888 registration works in one surface but fails in production, or when new members must be synced to the real game-provider API.

## Surfaces to inspect
- Laravel registration: `app/Http/Controllers/Auth/RegisterController.php`, route `/register`, table `users`.
- Legacy mobile registration: `mobile/function/daftar_akun.php`, form `mobile/template/register.php`, tables `tb_user`, `tb_saldo`, `tb_bank`.
- Legacy desktop registration: `dekstop/function/daftar_akun.php`, form `dekstop/template/register.php`, tables `tb_user`, `tb_saldo`, `tb_bank`.
- GameXaGlobal API wrapper: `app/Http/Api/gamexaglobal.php` and legacy `main/API/integration.php`.

## Provider sync pattern
Create/sync provider player before treating registration as successful:
- `POST /api/players` with complete payload: `agent_code`, `player_id`, `user_id`, `user_code`, `username`, `player_name`, `full_name`, `name`, `email`, `password`, `phone`, `currency`, `language`, `status`.
- If create returns duplicate/already-exists, verify with `GET /api/players?search=<extplayer>&page=1&limit=10` and accept exact username match.
- Balance checks use `GET /api/players/{id}/balance` after resolving numeric provider player id.
- Never log or print tokens/agent credentials; only report `[SET]` or `[REDACTED]`.

## Database sync pattern
Laravel `/register` should keep legacy tables in sync for the imported PHP surfaces:
- `users` for Laravel auth.
- `tb_user` with `status='Active'`, `status_game='ongame'`, `refferal=<extplayer>`.
- `tb_saldo` with zero balances.
- `tb_bank` with submitted payment fields.

Legacy mobile/desktop registration should also insert/update `users`, while preserving its existing inserts into `tb_user`, `tb_saldo`, and `tb_bank`.

## Production error pitfalls found
- Do not assume form sends `ip_register`; fallback to `request()->ip()` in Laravel.
- Do not insert columns just because the Eloquent model has them in `$fillable`; inspect live schema with `SHOW COLUMNS`. In this case `users.token` existed in code but not in live DB, causing `SQLSTATE[42S22] Unknown column 'token' in 'INSERT INTO'`.
- Imported Laravel logs may contain old unrelated stack traces; reproduce once, then tail newest entries and match the current timestamp.
- Live production uses Docker-baked source. After editing host files, run `docker compose build ksr888-web` and `docker compose up -d --no-deps --force-recreate ksr888-web`, then clear cached Laravel files manually if artisan is unreliable.

## Verification recipe
1. `GET https://ksr888.online/register`, extract CSRF token.
2. `POST /register` with a unique 6-12 char username, email, password + confirmation, phone, account name, bank, account number, captcha, and terms.
3. Expected: HTTP `302` to `https://ksr888.online/slots/server-b/5g/SL`.
4. Follow redirect; expected HTTP `200`, `gamesContainer`, and `MAIN SEKARANG` present.
5. Verify DB rows for the test username exist in `users`, `tb_user`, `tb_saldo`, and `tb_bank`.
6. Verify GameXaGlobal create/existing player path returns status 200/201 or exact existing player match; do not print secrets.
