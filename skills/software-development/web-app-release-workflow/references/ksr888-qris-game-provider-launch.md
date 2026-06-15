# KSR888 QRIS + Game Provider Launch Notes

Use this reference for Dockerized KSR888/Laravel production fixes around deposit QRIS, AutoGoPay webhooks, and provider game launches.

## Environment and release model
- Main repo: `/root/nusantara-ai-saas`; KSR888 source: `/root/nusantara-ai-saas/KSR888/site`.
- Web container: `nusantara-ai-saas-ksr888-web-1`; DB container: `nusantara-ai-saas-ksr888-db-1`.
- Source is baked into the Docker image, so after source changes run from `/root/nusantara-ai-saas`:
  - `docker compose build ksr888-web`
  - `docker compose up -d --no-deps --force-recreate ksr888-web`
- Host may not have PHP. PHP lint inside the container.
- Laravel `artisan` can be unreliable in this container; manual cache cleanup is acceptable:
  - `rm -f bootstrap/cache/config.php bootstrap/cache/routes-v7.php bootstrap/cache/services.php bootstrap/cache/packages.php`
  - `rm -f storage/framework/views/*.php`

## AutoGoPay QRIS lessons
- Keep provider secrets only in env; never echo real API keys/tokens in final responses.
- Runtime env must include `AUTOGOPAY_BASE_URL` and `AUTOGOPAY_API_KEY`; verify as `[SET]` only.
- Avoid Laravel POST route `/payment` because the public `/payment/` directory can trigger Apache redirects and bypass Laravel. Use a non-conflicting endpoint such as `/create-payment` while keeping callback wrappers under `/payment/webhook.php` if needed.
- Deposit amount normalizers must actually return the normalized value; a missing `return` can make the click handler silently stop before calling AutoGoPay.
- Webhook signature should prefer `AUTOGOPAY_CALLBACK_SECRET` but may need a fallback to `AUTOGOPAY_API_KEY` when no separate callback secret exists. Unsigned callbacks should return 401; signed valid callbacks should return 200.
- After creating a Laravel deposit/payment record, persist the AutoGoPay order mapping so webhook settlement can find and credit the transaction.

## Game provider launch lessons
- Provider listing routes may need to be public while actual launch remains protected. If a provider URL redirects to home, check for duplicate routes inside auth middleware overriding a public route.
- For 5G/GameXaGlobal, provider activation in DB matters: `providers.provider_status` must be `1` for the provider slug/code/type.
- GameXaGlobal launch may require the provider-side numeric player id, not the local username. If launch returns `Player not found`, create/resolve the player, clear related cache, then retry with the fresh numeric id.
- Player create payload may require multiple aliases/fields (`agent_code`, `player_id`, `user_id`, `user_code`, `username`, `player_name`, `full_name`, `name`, `email`, `password`, `phone`, `currency`, `language`, `status`).
- Normalize malformed launch hosts returned by provider APIs when verified safe, e.g. replace `api.httpsgamexaglobal.net` with `api.gamexaglobal.com` before redirect.

## Verification checklist
- `curl -i https://ksr888.online/slots/server-b/5g/SL` should be HTTP 200, not 302 to home.
- Guest page can show login-alert state; authenticated launch requires a real session/browser test.
- Grep compiled/live output for removed popup/banner text after clearing Blade cache.
- Check Laravel and Docker logs for provider errors such as `Player not found`, `launch rejected`, malformed URL, or webhook signature failures.
