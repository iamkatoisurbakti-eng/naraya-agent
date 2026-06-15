# Affiliate Dashboard Release Notes

Session-specific notes for the Nusantara AI affiliate dashboard rollout.

## Backend
- New auth-protected endpoint: `GET /api/payments/affiliate`
- Response shape now nests the wallet under `affiliate.wallet` and includes:
  - `referralLink`
  - `stats` (`referredUsers`, `paidReferrals`, `totalEarnings`, `pendingBalance`, `availableBalance`, `withdrawn`)
  - `referrals` (latest 20)
  - `earnings` (latest 20)
  - `withdrawals` (latest 10)
- `referralLink` uses the app origin plus `?voucher=<CODE>`.
- The endpoint calls payment-state sync first so paid orders are reflected before rendering wallet stats.

## Frontend
- Dashboard added a dedicated `Affiliate` section and quick-card entry.
- Affiliate page includes:
  - copyable referral link
  - wallet summary
  - referral list
  - earnings history
  - withdrawal history
- Registration modal pre-fills voucher code from `?voucher=` or `?ref=` in the current URL.

## Testing pitfalls
- Use unique test emails; reusing a seeded/demo email can cause 409 `EMAIL_EXISTS`.
- In affiliate tests, the API response is nested as `affiliate.wallet.voucherCode`, not `affiliate.voucherCode`.
- If you seed a paid order manually, ensure the buyer account actually exists before inserting the order.
