# AutoGoPay checkout flow smoke notes

Session learnings for `checkout.starlinkindonesia.shop`.

## Live endpoints
- Public checkout page: `https://checkout.starlinkindonesia.shop`
- Create payment: `POST /api/payments/autogopay/public/checkout`
- Poll status: `GET /api/payments/autogopay/public/orders/{id}/status`

## Verified behavior
- Public page returned `200 OK` with `Server: Caddy`.
- A valid checkout request returned `201` with fields such as:
  - `payment.id`
  - `qrString`
  - `qrUrl`
  - `providerReference`
  - `providerOrderId`
  - `status: pending`
- The status endpoint returned `200` and `providerStatus: pending` for the created order.

## Pitfall discovered
- The live HTML used a fixed amount of `14505729`.
- The backend rejected that request with:
  - `400 AUTOGOPAY_ERROR`
  - `amount exceeds maximum limit of Rp 10,000,000`
- This means the UI can appear live while the payment flow is still broken because the frontend amount exceeds provider limits.

## Quick smoke probe
```bash
python - <<'PY'
import json, urllib.request
payload = {
  'name': 'Test User',
  'phone': '081234567890',
  'email': 'test@example.com',
  'packageLabel': 'Test Package',
  'amount': 1000000,
  'notes': 'Smoke test',
}
req = urllib.request.Request(
  'https://checkout.starlinkindonesia.shop/api/payments/autogopay/public/checkout',
  data=json.dumps(payload).encode(),
  headers={'Content-Type':'application/json','Accept':'application/json','User-Agent':'Mozilla/5.0'},
  method='POST',
)
with urllib.request.urlopen(req, timeout=30) as r:
  print(r.status)
  print(r.read().decode())
PY
```
