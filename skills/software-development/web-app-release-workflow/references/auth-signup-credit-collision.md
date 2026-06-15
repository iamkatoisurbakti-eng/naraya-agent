# Auth signup credit collision: register/Google Sign-In 500

## Symptom
- Email register returns `500` with `SQLITE_CONSTRAINT_UNIQUE`.
- Google Sign-In succeeds at Google credential verification/user creation but fails before dashboard redirect.
- Frontend may show `Terjadi kesalahan server` or stay in auth modal.

## Root cause pattern
- User creation was followed by `grantSignupCredits()`.
- Existing live SQLite data contained a legacy ledger row with `reference_id = 'signup_bonus'` and `reason = 'payment'`.
- `credit_ledger` has `UNIQUE(reference_id, reason)`, so a non-idempotent bonus ledger insert can break the whole auth flow after the user has already been inserted.

## Investigation recipe
1. Reproduce with a fresh email:
   ```bash
   EMAIL="debug-$(date +%s)@example.com"
   curl -sS -i -X POST http://127.0.0.1:3000/api/auth/register \
     -H 'Content-Type: application/json' \
     --data "{\"email\":\"$EMAIL\",\"name\":\"Debug User\",\"password\":\"DebugPass123!\"}"
   ```
2. Inspect ledger duplicates and schema inside the container:
   ```bash
   docker compose exec -T app node - <<'NODE'
   const Database=require('better-sqlite3');
   const db=new Database('/app/data/nusantara-ai.db');
   console.log(db.prepare('PRAGMA table_info(credit_ledger)').all().map(c=>c.name+':'+c.type).join(','));
   console.log(db.prepare("select reference_id, reason, count(*) c from credit_ledger group by reference_id,reason having c>0 order by created_at desc limit 10").all());
   NODE
   ```
3. To isolate Google redirect failures without a real Google token, call `loginWithGoogle()` directly from built code and verify it returns session tokens.

## Fix pattern
- Use per-user references for signup grants: `signup_bonus:<userId>`.
- Make credit additions idempotent by inserting ledger first:
  - `INSERT OR IGNORE INTO credit_ledger ...`
  - if `changes === 0`, return the existing account without updating balance
  - only increment `credit_accounts.balance` / `lifetime_purchased` when the ledger insert succeeds
- This avoids double credit and prevents post-user hooks from breaking auth sessions.

## Verification
- `npm run build:server && npm run build:web`
- `bash scripts/deploy.sh`
- Fresh register returns HTTP 200 and includes access/refresh tokens.
- Fresh login returns HTTP 200 and includes access/refresh tokens.
- Simulated `loginWithGoogle()` returns access/refresh tokens.
- Health endpoints and Docker status are OK.
