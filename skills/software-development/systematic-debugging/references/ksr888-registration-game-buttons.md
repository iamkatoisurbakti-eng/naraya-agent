# KSR888 registration, GameXaGlobal sync, and game play button checklist

Use this reference when fixing KSR888 registration, provider pages, or game launch/play button visibility in `/root/nusantara-ai-saas/KSR888/site`.

## Runtime/deploy facts
- The live KSR888 web app is baked into the `ksr888-web` Docker image; edit source, then run from `/root/nusantara-ai-saas`:
  - `docker compose build ksr888-web`
  - `docker compose up -d --no-deps --force-recreate ksr888-web`
- Clear Laravel caches manually if `artisan` fails with ConsoleOutput/TTY issues:
  - remove `bootstrap/cache/config.php`, `bootstrap/cache/routes-v7.php`, `bootstrap/cache/services.php`, `bootstrap/cache/packages.php`, and `storage/framework/views/*.php` inside the container.
- Never print GameXaGlobal token/agent code, AutoGoPay keys, or DB credentials.

## Registration surfaces to check
There are multiple registration paths; keep them all consistent:
- Laravel `/register`: `app/Http/Controllers/Auth/RegisterController.php`
- Legacy mobile: `mobile/function/daftar_akun.php`
- Legacy desktop: `dekstop/function/daftar_akun.php`

## GameXaGlobal registration sync pattern
- On successful registration, create/sync provider player with GameXaGlobal `POST /api/players` before considering the registration complete.
- Payload should include the full provider-required field set:
  - `agent_code`, `player_id`, `user_id`, `user_code`, `username`, `player_name`, `full_name`, `name`, `email`, `password`, `phone`, `currency=IDR`, `language=id`, `status=1`.
- If create returns duplicate/already-exists, verify with `GET /api/players?search=<extplayer>&page=1&limit=10` and accept only an exact username match.
- Verify balance/user existence with `GET /api/players/{id}/balance` or the local helper `user_info()`; redact IDs/tokens in user-facing output.

## Local DB sync pattern
After a successful GameXaGlobal sync, keep Laravel and legacy DB tables aligned:
- Laravel table: `users`
- Legacy tables: `tb_user`, `tb_saldo`, `tb_bank`
- Check the live schema before inserting; production `users` did not have a `token` column, and `ip_register` may be absent from form POST and should fall back to `request()->ip()`.
- Successful Laravel registration should redirect to `/slots/server-b/5g/SL` so the user lands in the game lobby.

## Play button visibility pattern
Provider/category and detail pages use separate Blade views; patch all relevant surfaces:
- Category/provider list pages: `resources/views/slots/other.blade.php` and `resources/views/slots/provider.blade.php`
- Detail game grids: `resources/views/slots/games.blade.php` and `resources/views/slots/server-b.blade.php`
- Desktop overlays can be hidden until hover; force `.btn-wrapper`, `.game-overlay`, and `.game_button_play` visible when the user asks for always-visible buttons.
- Mobile often renders cards without overlay text; add explicit `MAIN SEKARANG` spans/buttons such as `provider-play-now-btn` or `mobile-play-now-btn` under each card.

## Verification
- Lint changed PHP/Blade files with PHP CLI in a container if host `php` is missing:
  - `docker run --rm -v /root/nusantara-ai-saas/KSR888/site:/app php:8.2-cli php -l /app/path/to/file.php`
- For registration, perform a live `/register` POST with a unique test username, confirm 302 to `/slots/server-b/5g/SL`, then verify rows exist in `users`, `tb_user`, `tb_saldo`, `tb_bank`, and `user_info(<username>)` returns status 200.
- For play buttons, probe representative URLs with desktop and mobile user agents:
  - `/slots`, `/casino`, `/sports`, `/fishing`, `/p2p`, `/lottery`, `/hot`, `/slots/server-b/5g/SL`
  - confirm `MAIN SEKARANG` counts are non-zero and mobile-specific button classes appear.
