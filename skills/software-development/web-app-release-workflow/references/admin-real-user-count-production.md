# Admin Real User Count in Production

Session pattern from Nusantara AI SaaS (`/root/nusantara-ai-saas`): admin dashboard showed inflated total user counts because live smoke-test accounts created during provider/payment verification remained in the production SQLite database.

## Problem
- Admin summary used `SELECT COUNT(*) FROM users`, which counted temporary smoke users such as:
  - `*@example.test`
  - `*@test.local`
  - `smoke-%@example.com`
  - `live-smoke-%@example.com`
  - `openai-smoke-%@example.com`
- User wanted admin dashboard moved/confirmed as live production and showing real production users.

## Fix pattern
1. Verify live runtime mode first:
   - public `/api/health` should report `env: live-production`.
   - container `NODE_ENV` should be `live-production`.
2. Query production DB counts directly from the app container before patching:
   - total users
   - role counts
   - recent users
   - count of known smoke/test email patterns
3. If production contains only agent-created smoke accounts matching deterministic patterns, delete those rows from `users`; FK cascades remove related tokens/credits/history where applicable.
4. Patch admin summary to expose both values when useful:
   - `totalUsers`: real/customer users, excluding smoke/test patterns.
   - `totalRegisteredUsers`: raw registered count for audit/debug.
   - `newUsersToday`: real/customer users created today, excluding smoke/test patterns.
5. Apply the same real-user filter to top-user/admin lists so smoke accounts do not appear in production leaderboards.
6. Patch UI copy to say `Total User Real` and mention live production / auto-refresh, so the admin can tell it is not demo data.

## Safe SQL filter example
```sql
lower(email) NOT LIKE '%@example.test'
AND lower(email) NOT LIKE '%@test.local'
AND lower(email) NOT LIKE 'smoke-%@example.com'
AND lower(email) NOT LIKE 'live-smoke-%@example.com'
AND lower(email) NOT LIKE 'openai-smoke-%@example.com'
```

Use this only for known agent-created smoke accounts. Do not delete or hide ambiguous customer accounts without explicit review.

## Verification
- `npm run build:server && npm run build:web`
- `NODE_ENV=test ... jest --runInBand tests/api`
- `bash scripts/deploy.sh`
- Verify:
  - `/api/health` -> `live-production`
  - `/api/admin/summary` with an admin token -> `productionLive: true`
  - `totalUsers` equals the filtered real user count from SQLite
  - app container is healthy
