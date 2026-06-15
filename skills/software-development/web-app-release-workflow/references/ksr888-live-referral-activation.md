# KSR888 live referral activation

Use this when the user asks to make KSR888 referral / refferal live active.

## Context
- App path: `/root/nusantara-ai-saas/KSR888/site`.
- Docker service: `ksr888-web` from `/root/nusantara-ai-saas/docker-compose.yml`.
- Referral spellings in code are legacy: `refferal`, `reff`, and `referral` all appear.
- Tables/columns observed live:
  - `users`: `extplayer`, `name`, `email`, `ref_code`, `status_reff`, `ref_link`, `last_login`, `first_deposit`, `last_deposit`.
  - `networks`: `user_id`, `username`, `ref_code`, `parent_id`, `last_login`, `first_deposit`, `last_deposit`.

## Implementation pattern
1. Make referral identity self-healing when a logged-in user opens `/refferal`:
   - generate `users.ref_code` if missing,
   - set `users.ref_link` to `/referral-register?ref=<ref_code>`,
   - set `users.status_reff = 1`,
   - set `email_verified_at` if the old flow used it as approval gate.
2. Accept referral input by more than one legacy key:
   - `ref_code` form field,
   - query `ref`,
   - query `reff`,
   - and match sponsor by `users.ref_code`, `users.name`, or `users.extplayer`.
3. On registration, use `Network::updateOrCreate(['user_id' => $newUser->id], ...)` instead of raw `create()` so retries do not duplicate downline rows.
4. Add a live JSON endpoint such as `/refferal/live-summary` returning status, `ref_code`, `ref_link`, `downline_total`, and server time for frontend refresh.
5. For unauthenticated `/refferal`, return a redirect or 401 response before touching `Auth::user()`; otherwise public smoke tests can hit a 500.
6. Use a partial Blade table for `/getReferralDownline` AJAX so date filtering can replace only the table.

## Verification
- Rebuild: `docker compose up -d --build ksr888-web`.
- Lint in container: `docker compose exec -T ksr888-web sh -lc 'php -l app/Http/Controllers/RefferalController.php && php -l app/Http/Controllers/OtpController.php && php -l app/Http/Controllers/Auth/RegisterController.php && php -l app/Models/User.php'`.
- Clear Laravel cache with PTY if non-TTY fails: `docker compose exec ksr888-web php artisan optimize:clear --no-ansi`.
- Smoke checks:
  - `curl -k -s -o /tmp/ksr_ref_register.html -w '%{http_code}\n' 'https://ksr888.online/referral-register?ref=SMOKETEST'` should be `200`.
  - `curl -k -s -o /tmp/ksr_refferal.html -w '%{http_code}\n' 'https://ksr888.online/refferal'` should be `302` unauthenticated, not `500`.
  - render `RefferalController::liveSummary()` in-container after `Auth::login($user)` for JSON proof.
- Check logs for new `fatal|parse error|syntax error|SQLSTATE|undefined|500|refferal` entries.

## Pitfalls
- The route name `refferal.submit` was originally declared in `routes/api.php`; Blade forms using `route('refferal.submit')` need a web route when submitting from session/CSRF-authenticated pages.
- `Transaksi::where('user_id', ...)->orWhere('user_name', ...)->where('status', 2)` must group the OR in a closure; otherwise status filtering applies only to the second condition.
- The `User` model may have `$fillable` rather than relying on `$guarded`; include `extplayer`, `ref_link`, `status_reff`, `email_verified_at`, `ip_register`, `captcha`, and `token` before mass assigning them.
