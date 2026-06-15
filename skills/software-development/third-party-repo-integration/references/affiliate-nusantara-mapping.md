# Affiliate repo mapping for Nusantara AI

Vendor repo cloned:
- `vendor/affiliate-management-system`

What it provides:
- AffiliateEngine orchestrator
- affiliate/referral/commission/payment/fraud/analytics modules
- examples for basic affiliate, commission tracking, payout flows

Nusantara mapping:
- `AffiliatePanel` -> affiliate dashboard, referral link, stats, withdrawals
- `vouchers` / `voucher_referrals` -> referral ownership and signup attribution
- `affiliate_earnings` -> commission ledger with 7-day availability hold
- `wallet_withdrawals` -> payout requests and status
- `payment_orders.affiliate_amount` -> commission generated from paid orders

Practical guidance:
- Prefer reusing the existing payment/referral tables instead of copying the vendor's whole engine.
- Keep the host app's checkout flow as source of truth for paid-order events.
- Split affiliate-specific routes into their own router when the payment router becomes too crowded.
- Keep legacy affiliate endpoints alive during migration if the frontend already depends on them.
