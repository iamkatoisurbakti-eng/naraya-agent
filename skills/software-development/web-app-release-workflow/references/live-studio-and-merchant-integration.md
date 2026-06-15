# Live Studio + Merchant Integration Notes

Context: Dockerized React + Express app where sidebar items were placeholders and billing needed AutoGoPay checkout support.

## Live sidebar studios
- Do not leave sidebar items as inert `<a href="#">` links. Use explicit active section state and `<button type="button">` controls so Images, Video, Music, Chat, and Clipper render usable panels.
- Add a reusable studio panel instead of duplicating UI per medium. Map section -> capability:
  - Images -> `image`
  - Video -> `video`
  - Music -> `audio`
  - AI Chat -> `text`
- Backend route pattern:
  - `POST /api/generate` behind `requireAuth`
  - validate `capability` and prompt length
  - route text to OpenAI/Anthropic, image/video to FAL, audio to ElevenLabs or configured provider
  - return provider-not-configured `503` when env keys are missing instead of silently demoing
- Add `GET /api/generate/status` to expose configured providers without leaking secrets.
- If generated media URLs or base64 audio are rendered in the browser, update CSP, especially `mediaSrc: ["'self'", 'data:', 'https:']`.
- E2E selectors can duplicate when the active section title is shown in both header and panel. Scope by heading level or section, e.g. `getByRole('heading', { name: 'Images Studio', level: 1 })`.

## Provider env passthrough in Docker Compose
- Adding code that reads new provider env vars is not enough. Also pass them through in `docker-compose.yml` so production containers can see them:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `FAL_KEY` / `FAL_API_KEY`
  - `ELEVENLABS_API_KEY`
  - `ELEVENLABS_VOICE_ID`
- Add placeholder keys to `.env.example` and `.env.production`, but never echo real values in chat/log summaries.

## AutoGoPay merchant pattern
- Store payment orders server-side before/after checkout via a `payment_orders` table with: `id`, `user_id`, `provider`, `plan_id`, `amount`, `currency`, `credits`, `status`, `checkout_url`, `provider_reference`, `raw_response`, timestamps.
- Use auth-protected API routes:
  - `GET /api/payments/plans`
  - `GET /api/payments/orders`
  - `POST /api/payments/autogopay/checkout`
- Webhook route is public but should verify HMAC-SHA256 signature when configured:
  - `POST /api/payments/autogopay/webhook`
- Config/env shape used:
  - `AUTOGOPAY_BASE_URL` (observed production gateway shape: `https://v1-gateway.autogopay.site`)
  - `AUTOGOPAY_MERCHANT_ID`
  - `AUTOGOPAY_API_KEY`
  - `AUTOGOPAY_SECRET_KEY` / callback secret when provided
- Docs-specific QRIS flow seen at `https://autogopay.site/docs`:
  - generate QRIS with `POST /qris/generate`
  - check status with `POST /qris/status`
  - sign JSON payload with HMAC-SHA256 using the AutoGoPay API key when docs require `signature`
  - persist provider response but never echo merchant/API keys in chat or logs
- Normalize provider response defensively because gateway names vary: accept `qr_url`, `qris_url`, `qr_image`, `qr_string`, `checkout_url`, `payment_url`, `transaction_id`, `reference`, `reference_id`, or `id`.
- UI should render QRIS/payment links directly and display a clear “merchant not configured” message when env vars are empty, not pretend payment is live.
- Smoke verification can create a disposable account, call authenticated `GET /api/payments/plans`, and assert `provider: autogopay`, `mode: qris`, `configured: true`; print tokens/secrets only as `[REDACTED]`.

## Verification
- Run `npm run typecheck` before deeper tests after adding routes/types.
- Run API tests, web build, e2e, live test, then deploy.
- After deploy verify:
  - public health endpoint OK
  - unauthenticated payment plans returns 401
  - Docker app container reaches `healthy`
