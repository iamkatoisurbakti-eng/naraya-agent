# Subscription pricing overrides and public field hygiene

Use this note when changing Nusantara-style subscription/top-up prices.

## Pattern
- Keep internal API/provider cost available server-side for accounting, but do not expose it in customer UI or public plan JSON.
- If a plan needs a specific customer-facing price that differs from a multiplier-derived value, add an explicit per-plan `amount` override.
- `toPaymentPlan()` / public plan responses should return only customer-facing fields such as `id`, `name`, `credits`, `amount`, `currency`, `description`, and `isFree`.
- Checkout must use the same final customer-facing amount as the plan card. Apply voucher/affiliate calculations to this amount, not to the old derived formula.
- Keep persisted payment order accounting fields if needed (`cost_amount`, `selling_multiplier`), but avoid returning them in public plan/checkout responses unless explicitly needed for admin-only screens.

## Verification
1. Build server/web and run API tests.
2. Deploy through the project script.
3. Register a disposable smoke user, fetch `/api/payments/plans`, and assert:
   - updated plan `amount` equals the requested final price
   - plan order is unchanged except intended changes (for example Free first)
   - public plan payload does not include `apiCost`, `originalAmount`, or `sellingMultiplier`
4. Clean the disposable smoke user from live SQLite after verification.
