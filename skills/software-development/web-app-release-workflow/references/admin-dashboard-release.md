# Admin dashboard release notes

Use when adding `/admin` or similar owner/operator dashboards to the Dockerized React + Express app.

## Pattern used
- Add frontend route `/admin` in `web/src/main.tsx` and a dedicated component under `web/src/components/AdminDashboardPage.tsx`.
- Keep admin UI behind existing auth token. If no token, redirect to `/`; if token exists but role is not admin, show the backend error.
- Add an auth-protected backend endpoint such as `/api/dashboard/admin/summary` that checks `req.user.role === 'admin'` before querying global app data.
- Admin stats that are useful without new tables:
  - users/admin users/active users today
  - total and today generations from `generation_history`
  - total/paid orders and IDR revenue from `payment_orders`
  - credit balances/purchased/used from `credit_accounts`
  - recent users and recent orders
  - generations grouped by capability
- For visitor analytics, add one small table and best-effort middleware:
  - `visitor_events(id, visitor_key, path, referer, user_agent, ip_hash, created_at)`
  - indexes on `created_at` and `visitor_key`
  - middleware for `GET` SPA/public pages only, not `/api/*`, `/assets/*`, or static file paths
  - HTTP-only long-lived cookie such as `nusantara_vid` for unique visitors
  - hash IP/remote address before storage; do not store raw secrets or credentials
  - catch/ignore insert failures so analytics never blocks the site
  - expose visitor cards from `/api/dashboard/admin/summary`: unique visitors today, views today, total unique visitors, total views

## Access control, login, and verification
- Verify `/admin` serves the SPA HTML publicly, but the data endpoint requires auth.
- Verify `/api/dashboard/admin/summary` without auth returns 401.
- Verify a non-admin authenticated user receives 403 `ADMIN_REQUIRED`.
- Admin users are determined by `ADMIN_EMAILS`; if the env is not set, only the config default applies. Existing users may need login/role refresh or a DB role update before they can access admin data.
- To explain admin login to the user: register/login on the normal site using an email in `ADMIN_EMAILS`, then open `/admin`. If the admin email is listed but not in the `users` table, tell them to register with that email first.
- Do not print secrets or env values; report only `set/missing` for admin/payment/provider envs.

## SQLite/schema pitfall
- Before inserting credit ledger rows, inspect the live table columns. In this repo the ledger schema uses:
  `id, user_id, amount, balance_after, reason, reference_id, reference_type, description, metadata, created_at`
  and not older fields like `type` or `metadata_json`.
- If register/login fails with `SQLITE_ERROR` after billing/credit changes, test credit-service inserts against the actual table and patch `addPurchasedCredits`/`spendCredits` to match the schema.

## Production checks
- `npm run build:server && npm run build:web`
- `bash scripts/deploy.sh`
- `curl` local and public `/api/health`
- `docker compose ps`
- `curl https://<domain>/admin` to confirm SPA route fallback works
- grep built JS bundle for admin UI copy and `/api/dashboard/admin/summary`
