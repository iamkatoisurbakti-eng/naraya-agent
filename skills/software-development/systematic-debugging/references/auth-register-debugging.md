# Auth/register debugging note

## Fast reproduction
1. POST `/api/auth/register` with email, name, password.
2. Capture the returned `accessToken` and call `GET /api/auth/me` with `Authorization: Bearer <token>`.
3. If both succeed, the backend register flow is healthy and the bug is likely in the frontend form, cached bundle, or client-side validation.

## Observed lesson
- In the Nusantara AI SaaS session, live register returned `200` and `/api/auth/me` returned `200` with the new token.
- That means a reported "daftar akun error" can be a stale browser/frontend problem even when the API is fine.

## What to check next
- Browser console/network for the register request.
- Cached frontend bundle vs current deployed build.
- Client validation: email format, password length, required name field.
- Whether the UI is sending the `voucherCode` field unexpectedly or blanking payload keys.
