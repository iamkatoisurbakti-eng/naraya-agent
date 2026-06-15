# Payment history + live credit sync

Use this reference when a Dockerized React/Express app has QRIS/top-up payments and the user asks for live production credit sync, user payment history, or automatic top-up after callback.

## Backend pattern

1. Keep `payment_orders` as the source of truth for top-up history.
2. Expose an auth-protected user endpoint such as `GET /api/payments/orders` that returns the current user's recent orders only:
   - `id`, `provider`, `planId`, `amount`, `currency`, `credits`, `status`
   - `checkoutUrl` / `qrUrl`, `providerReference`
   - `creditedAt`, `createdAt`, `updatedAt`
3. Before returning dashboard/payment history, reconcile pending orders for that user with the provider using a bounded refresh:
   - filter `provider = 'autogopay'`
   - filter `status = 'pending'`
   - require `provider_reference IS NOT NULL`
   - throttle by `updated_at` (for example older than 8 seconds)
4. Make credit grants idempotent:
   - export/use a single `creditPaidOrder(orderId)` helper
   - only grant when `status = 'paid'` and `credited_at IS NULL`
   - ledger reference should be the order id with reason `purchase`
   - set `credited_at = CURRENT_TIMESTAMP` after grant
5. Add a user sync helper (`syncUserPaymentState(userId)`) that:
   - refreshes pending provider orders for that user
   - credits any paid-but-uncredited orders
6. Call that helper from dashboard summary and payments orders endpoints so stale paid QRIS is fixed even if the webhook was missed.

## Webhook/callback pattern

- Verify signature when a provider signature header is present/configured; do not leak webhook secrets.
- Accept common provider payload shapes defensively:
  - `transaction.id`
  - `transaction.transaction_id`
  - `data.transaction_id`
  - top-level `transaction_id`
  - `order_id`
  - `transaction_status` or `status`
- Normalize provider statuses (`settlement`, `success`, `completed` → `paid`; failure/expiry values → `failed`).
- Match by provider reference first. If missing, match by local `order_id` and amount before updating.
- After status becomes `paid`, call the same idempotent credit helper; never duplicate crediting logic in the webhook.
- Support provider verification challenges with a simple `{ success: true }` response.

## Frontend pattern

1. In the billing/subscription panel, fetch `GET /api/payments/orders` on mount.
2. Render a user-visible `History Pembayaran` list showing plan, amount, credits, status, transaction id, created time, and `creditedAt` if present.
3. Poll every ~5 seconds while there is an active payment or pending order.
4. When the active order becomes `paid`, show a success message and call an `onPaymentSync` callback to reload dashboard summary/credit widgets.
5. Add a manual Refresh button for user confidence.

## Verification

- `npm run build:server && npm run build:web`
- relevant API tests
- deploy with the project script
- smoke production:
  - `/api/health` reports live production
  - register/login smoke user without printing token
  - `/api/dashboard/summary` returns `paymentHistory` as an array
  - `/api/payments/orders` returns only that user's orders
  - webhook verification/challenge endpoint responds OK
  - DB query shows `paid` orders with `credited_at IS NULL` count is 0
  - revenue total is derived from `payment_orders.status = 'paid'`

## Pitfalls

- A frontend-only payment history is not enough; dashboard summary must also sync paid orders so credit widgets become live.
- Do not grant credit on order creation; grant only after provider status is paid.
- Do not require one exact webhook JSON shape unless the provider docs guarantee it; QRIS/merchant callbacks often vary by environment.
- Do not print tokens, API keys, provider webhook secrets, or raw payment credentials in final responses or logs.
