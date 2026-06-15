# PHP host AutoGoPay rollout on ksr888.online

Use this when adding a payment flow to the imported PHP+MariaDB host inside the Nusantara AI SaaS repo.

What changed
- Added PHP endpoints under `KSR888/site/payment/` for QRIS create, status polling, and webhook handling.
- Because Apache serves `KSR888/site/public` as the docroot, public shims must exist under `KSR888/site/public/payment/` for every browser-called endpoint (`create_qris.php`, `order_status.php`, and `webhook.php`) and simply require the real file from `../../payment/...`; otherwise `/payment/create_qris.php` returns the Laravel/redirect-style 404 even though the real backend file exists.
- Added `tb_autogopay_orders` in the MariaDB schema to track provider reference, QR URL/string, status, raw response, expiry, and paid timestamp.
- Wired the desktop/mobile deposit pages to offer `BAYAR VIA QRIS` alongside the legacy manual-upload deposit path.
- Excluded `metode = 'AutoGoPay QRIS'` rows from the manual backoffice pending-deposit queue; history still shows them.

Critical deploy pitfalls
1. `ksr888-web` needs explicit `AUTOGOPAY_*` env passthrough in `docker-compose.yml`.
   - The Node app already had these vars, but the PHP host did not.
   - Without passing `AUTOGOPAY_BASE_URL`, `AUTOGOPAY_API_KEY`, `AUTOGOPAY_MERCHANT_ID`, and `AUTOGOPAY_CALLBACK_SECRET`, the PHP endpoints return `503 AutoGoPay belum dikonfigurasi` even though the main app works.
2. Recreating `ksr888-web` without sourcing `.env.production` can silently inject the compose fallback DB password (`change-me-ksr888`).
   - Symptom: whole host starts returning `500` with Apache/PHP logs showing `Access denied for user 'ksr888_user'@'<container-ip>'` from `function/connect.php`.
   - Fix: source `.env.production` before `docker compose up -d --force-recreate ksr888-web`, then verify inside the container that `DB_PASSWORD` matches production.
3. User login on the PHP frontends does **not** set `$_SESSION['status'] = 'login'`.
   - Frontend user auth should key off `$_SESSION['extplayer']` and `$_SESSION['id']`, not the admin-style `status` session flag.
   - Otherwise new authenticated AJAX endpoints falsely return `401 Silakan login terlebih dahulu` right after a successful user login.

Verification recipe
- Check live host pages first:
  - `https://ksr888.online/` -> 200
  - `https://ksr888.online/mobile/index.php?page=register` -> 200
  - unauthenticated `GET https://ksr888.online/payment/create_qris.php` -> 405 (route exists)
- Register a throwaway user, log in, then POST to `/payment/create_qris.php` with:
  - `nominal=30000`
  - `bonus=tanpabonus`
  - headers `Accept: application/json`, `X-Requested-With: XMLHttpRequest`
- Expect `201` with `order.orderId`, `providerReference`, `checkoutUrl/qrUrl`, and `status=pending`.
- Poll `/payment/order_status.php?order_id=<id>` and expect `200` with the same order shape.
- For end-to-end proof without waiting for a real payer, send a signed webhook payload to `/payment/webhook.php` using `AUTOGOPAY_CALLBACK_SECRET`; expect the order to transition to `paid` and `tb_transaksi.status` to become `Sukses`.

Useful live checks
- Inside `ksr888-web`:
  - print `DB_PASSWORD`, `AUTOGOPAY_BASE_URL`, and whether `AUTOGOPAY_API_KEY` is set
  - run `php -l` against the new payment PHP files before finishing
- In MariaDB:
  - confirm `tb_autogopay_orders` exists
  - count `tb_transaksi` rows with `metode='AutoGoPay QRIS'`
  - count `tb_autogopay_orders` by status
