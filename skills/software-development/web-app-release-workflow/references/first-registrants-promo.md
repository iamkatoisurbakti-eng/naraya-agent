# First-registrants promo pattern

Use when a SaaS promo is defined as "first N registrants" rather than first N payers/orders.

## Backend
- Add a single env/config knob for the quota, for example `PROMO_FIRST_REGISTRANTS_LIMIT`, plus existing `PROMO_DISCOUNT_PERCENT`.
- Determine eligibility from the authenticated user's registration order/count, not from checkout attempts.
- Keep public promo status aggregate-only: `discountPercent`, `limit`, `used`, `remaining`, `headline`. Do not expose user rows, registration timestamps, internal API cost, margin, multiplier, or private order fields.
- `/api/payments/plans` should be authenticated when eligibility is user-specific. It can return customer-facing promo fields such as `promoEligible`, `promoDiscountPercent`, `promoDiscountAmount`, and final customer price.
- Checkout must recompute eligibility server-side and apply the promo automatically to the selling/customer price. Do not trust the frontend plan price.
- If vouchers can coexist, compute promo + voucher as a total discount and label it as `Total diskon` in customer UI.

## Frontend
- Landing copy should clearly say the promo is for the first N registrants and that checkout applies it automatically for eligible accounts.
- Billing should show a small promo banner with eligible/not-eligible state and remaining quota.
- Plan cards should show final customer-facing price; if showing a struck-through comparison price, ensure it is not an internal API cost/margin field.

## Verification
- Typecheck both server and web.
- Build web and server.
- Run API/unit/e2e tests relevant to auth, plans, checkout, and landing navigation.
- Verify the public promo endpoint on live.
- For React/Vite SPAs, do not rely on raw `curl` homepage HTML for landing copy; use Playwright or grep hydrated/bundled JS.
- If deploy e2e stubs omit fields like `creditCost`, normalize frontend model/credit values before calling `.toLocaleString()`.

## Nusantara-AI notes from the 2026-05-08 release
- The repo was not a git repo, so a manual backup directory was created before deploy.
- Deploy went through `npm run deploy`, which ran tests/builds and Docker Compose.
- Live verification checked `/api/health`, `/api/payments/promo`, Docker Compose health, and a Playwright mobile viewport (`390x844`) for promo text and no horizontal overflow.
