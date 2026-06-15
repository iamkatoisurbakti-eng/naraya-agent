# KSR888 DB repair and footer panel notes

## Live DB auth repair when compose/env is correct but PHP still 500s
Observed pattern:
- DB container is healthy.
- PHP web container logs show `mysqli_sql_exception: Access denied for user ... (using password: YES)`.
- Recreating the web container alone does not fix it.

Useful recovery flow:
1. Stop the PHP and DB compose services to avoid locking the volume.
2. Start a disposable MariaDB container against the same named volume, but with `--skip-grant-tables --skip-networking=0`.
3. Inspect the current users:
   - `SELECT User,Host,Priv FROM mysql.global_priv WHERE User='...'`
4. Compare the stored `authentication_string` against `SELECT PASSWORD('expected-password');`.
5. If the DB user hash is stale or mismatched, update `mysql.global_priv` to the correct hash, then stop the disposable container.
6. Bring the real DB and PHP services back up and verify:
   - `docker exec <web> mariadb -u<user> -p<password> -e "SELECT 1;"`
   - `curl -I https://<host>/`

Notes:
- Use this only for your own owned/imported host when you have legitimate admin access.
- Prefer repairing the existing volume over deleting the database when the schema/content should be preserved.
- This worked on a KSR888-style imported PHP stack where the env values were correct but the DB grant table had drifted.

## Footer payment/browser panel pattern
- For KSR888-style footer chrome, a compact right-aligned panel works well:
  - left: `Cara Pembayaran`
  - cards: bank transfer, e-wallet, pulsa, QRIS
  - right: `Browser yang Disarankan` with Chrome/Firefox/Safari icons
- Use local assets already present in the host tree when possible:
  - `mobile/generated-assets/payment-types/BANK.svg`
  - `mobile/generated-assets/payment-types/EMONEY.svg`
  - `uploads/bank/qris.png`
  - brand SVGs for browser icons
- Keep the panel responsive by switching to a stacked grid on mobile and a horizontal flex row on desktop.
- The screenshot fit improves when the cards are fixed-width on desktop and 2-column on mobile.
