# Credits + ModelArk live-production release notes

Use this when turning a demo studio into a credit-metered, provider-backed live production app.

## Credit system pattern
- Add/verify persistent tables before wiring UI:
  - `credit_accounts(user_id, balance, lifetime_purchased, lifetime_used)`
  - `credit_ledger` / transactions with idempotent references
  - `generation_history(..., cost_credits, options_json, expires_at)`
  - `payment_orders(..., credits, original_amount, selling_multiplier, status)`
- New-user signup credit must be idempotent and per-user scoped. Avoid global references such as `signup_bonus` under a unique `(reference_id, reason)` constraint; use `signup_bonus:<userId>` or insert ledger row first with `INSERT OR IGNORE` and only update balance when a row was inserted.
- Generation routes should check credit balance before provider calls and consume credits only after a successful provider result.
- Suggested cost tiers used in this project:
  - text/chat: 5 credits
  - image: 25 credits
  - audio/music/voice: 40 credits
  - video: 250 credits
- Keep per-user generation history private (`WHERE user_id = ?`), cap dashboard display (for example latest 30 rows), and auto-expire rows after 30 days with `expires_at` plus cleanup on write/read.

## Payment/webhook pattern
- Backend plans should use base API cost as source of truth and derive `amount = apiCost * 5`.
- Persist `originalAmount`/`apiCost`, `sellingMultiplier`, final `amount`, currency, credits, provider, and plan id in the order row.
- Webhook/payment success must grant credits idempotently by order id; do not grant again when the same payment status callback is retried.
- Customer-facing cards should show IDR final price and package description. Only show internal base-cost/multiplier if the user explicitly asked for pricing transparency.

## ModelArk / OpenAI production wiring
- Keep ModelArk keys in env only. Support aliases: `ARK_API_KEY`, `BYTEDANCE_API_KEY`, `BYTEPLUS_API_KEY`.
- Pass env vars through `config.ts`, `docker-compose.yml`, `.env.example`, and `.env.production`; code-only reads are not enough in Docker.
- For ModelArk text calls, use `/api/v3/responses` with `model` such as `seed-2-0-pro-260328` or `seed-2-0-lite-260228` and parse `output_text` first, then fall back to output content arrays.
- When adding a friendly preset id like `dola-seed-2-0`, map/reroute it to the configured ModelArk default unless the provider accepts that exact id.
- Production smoke tests should register a temporary user, verify dashboard credit shape, fetch `/api/payments/plans`, then run a small authenticated `/api/generate` call with ModelArk and OpenAI. Print only status/provider/model/text-present booleans; never echo API keys or access tokens.

## Admin dashboard pattern
- `ADMIN_EMAILS` governs role assignment; refresh role at login/Google-login for existing users.
- Admin route should require auth plus role check and should aggregate safe metrics only: total users, paid revenue, paid orders, credits sold/used, top credit users, recent generation metadata.
- For admin auto-redirect in SPA dashboards, keep non-admin e2e fixtures as `role: user`; otherwise tests may land on Admin Dashboard and fail old dashboard selectors.

## Test/live pitfalls
- When dashboard copy changes, update both Playwright e2e and any shell/live-test selectors. A passing e2e does not mean `npm run test:live` selectors were updated.
- If a production SPA verification searches raw root HTML, remember Vite initial HTML may not contain React text. Grep built/live JS bundles or use Playwright DOM checks instead.
- If API tests pass but `test:live` fails, inspect the embedded stubs in `live-test.sh`; they often duplicate older e2e expectations.
