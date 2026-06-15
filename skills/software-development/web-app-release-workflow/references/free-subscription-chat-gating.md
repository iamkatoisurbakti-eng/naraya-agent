# Free subscription gating for Nusantara AI SaaS

Use when the user wants a default/free subscription tier while keeping paid features gated.

## Pattern used
- Add an automatic `Free` plan to `/api/payments/plans` as the first plan.
- Free plan public fields only: `id`, `name`, `credits`, `amount`, `currency`, `description`, `isFree`.
- Do not expose internal billing fields in plan/payment responses: `apiCost`, `originalAmount`, `sellingMultiplier`.
- Free plan description used: `Unlimited Chat AI dengan model gratis. Fitur lain membutuhkan subscription berbayar.`
- Free plan is not checkout-able; `/autogopay/checkout` should reject `plan.id === 'free'` with a clear message because it is automatic.

## Backend gating
- Centralize gating in `src/services/subscription-service.ts`:
  - paid/admin users: all features allowed.
  - free users: only `capability === 'text'` with `isFreeChatModel(model)` allowed.
  - otherwise throw `402 SUBSCRIPTION_REQUIRED`.
- Call `assertFeatureAccess(userId, role, capability, model)` before provider calls in `/api/generate` and before AI Clipper job creation.
- Keep `NODE_ENV === 'test'` permissive unless tests are updated for subscription gating; otherwise existing API tests for video/clipper will fail with 402.
- Add subscription metadata to `/api/generate/quote`: `subscription` and `requiresSubscription`, so UI can warn before generate.

## Free Chat AI interaction
- Keep the free-chat allowlist in `credit-service` as source of truth:
  - Kimi K2
  - Dola-Seed-2.0 Mini
  - Dola-Seed-2.0 Lite
  - DeepSeek V3.2
- Free chat models return `creditCost: 0`, render `Gratis`, sort above paid chat models, and successful generation must not debit balance.
- Non-free text models require paid subscription even if the user has some credits, unless the business rule changes.

## UI expectations
- Billing/Topup page shows Free as the first card.
- Free card price text: `Gratis`; action: `Aktif Otomatis` and disabled.
- Paid plan cards should show only customer-facing prices and credits.
- Avoid text like `Harga Jual`, `modal API`, `apiCost`, `originalAmount`, or multiplier formulas in public UI.

## Verification
1. `npm run build:server && npm run build:web`
2. `npx cross-env NODE_ENV=test DATABASE_FILE=/tmp/nusantara-ai-test.db JWT_SECRET=[REDACTED] jest --config jest.config.cjs --runInBand tests/api`
3. `bash scripts/deploy.sh`
4. Production smoke with a temporary `*@example.test` user:
   - `/api/payments/plans` first plan is `free` and lacks internal price fields.
   - `/api/generate/quote?capability=text&model=deepseek-v3-2-251201` returns cost `0`, `requiresSubscription:false`, plan `free`.
   - `/api/generate/quote?capability=video&model=seedance-2` returns `requiresSubscription:true` for free user.
   - free chat `/api/generate` succeeds with `creditCost:0`.
   - image/video/clipper calls return `402 SUBSCRIPTION_REQUIRED` for free user.
5. Clean temporary smoke users from live SQLite after verification.
