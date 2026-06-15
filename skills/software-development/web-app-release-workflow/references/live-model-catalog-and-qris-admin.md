# Live Model Catalog + QRIS Admin Production Notes

Session pattern from Nusantara AI SaaS (`/root/nusantara-ai-saas`): user needed production mode, live model/provider catalog, and admin revenue/QRIS data to update without manual refresh.

## Live model/provider catalog
- Do not rely only on a static `MODEL_CATALOG` when the user asks for “all models provided” by a provider.
- Keep stable/static entries for tests and known UI ordering, then append dynamic provider models from provider list endpoints:
  - OpenAI: `GET https://api.openai.com/v1/models` with `Authorization: Bearer $OPENAI_API_KEY`.
  - BytePlus/ModelArk: `GET ${ARK_BASE_URL:-https://ark.ap-southeast.bytepluses.com/api/v3}/models` with `ARK_API_KEY` or aliases `BYTEDANCE_API_KEY`/`BYTEPLUS_API_KEY`.
- Cache dynamic model lists briefly (for example 10 minutes) to avoid slow catalog calls on every page load.
- Disable dynamic provider fetches in `NODE_ENV=test` so tests that assert exact static catalog length remain deterministic.
- For OpenAI catalog display, filter to usable text/reasoning models (`gpt-4*`, `gpt-5*`, `o*`) and exclude audio/realtime/transcribe/TTS/search models unless the UI supports those capabilities.
- For ModelArk catalog display, map domains to capabilities: `LLM`/`VLM` -> text, `ImageGeneration` -> image, `VideoGeneration` -> video; skip `Shutdown` models.
- Important pitfall: ModelArk `/models` may list Kimi models (for example `kimi-k2-*`) even when the current account/endpoint cannot call them via `/chat/completions`. Always smoke-test the actual generation endpoint; if it returns `InvalidEndpointOrModel.NotFound`, report it as provider/account access not app routing.
- Never print API keys in verification. Use masked checks like `{ openai: true, ark: true }`, counts, and sample model ids only.

## OpenAI + ModelArk generation routing
- OpenAI text generation should accept both older `chat.completions` style models and newer model ids by detecting `gpt-*` and `o*`; use `gpt-4o-mini` as a conservative fallback when an unknown OpenAI model id is selected.
- ModelArk/Kimi text routing should pass through real provider model ids, not friendly aliases, unless the app maps aliases explicitly to a configured real model.
- For friendly aliases used in the UI, keep a backend alias map so generation calls route to actual ModelArk endpoint ids. Proven Nusantara examples: `dola-seed-2-0-mini -> seed-2-0-mini-260215`, `dola-seed-2-0-lite -> seed-2-0-lite-260228`, `deepseek -> deepseek-v3-2-251201`.
- If some Chat AI models are customer-free, encode the rule in the central credit service and reuse it for both quote and generation debit logic; do not only change labels. In the catalog route, sort preferred free text models to the top, but preserve deterministic static order under `NODE_ENV=test` if tests assert exact catalog order.
- For Nusantara, preferred free Chat AI top order is: Kimi K2, Dola-Seed-2.0 Mini, Dola-Seed-2.0 Lite, DeepSeek V3.2. UI should show `Gratis` for `creditCost === 0`, not `0 kredit`.
- Seedance/Seedream media routing should continue using the shared ModelArk key helper so `ARK_API_KEY`, `BYTEDANCE_API_KEY`, and `BYTEPLUS_API_KEY` all work in containers.

## QRIS/admin live production pattern
- Admin panel “live” should mean both frontend polling and backend reconciliation:
  1. Admin UI polls `/api/admin/summary` every ~5 seconds and has a manual refresh button.
  2. Backend summary refreshes a bounded number of pending QRIS/AutoGoPay orders before computing totals.
  3. Revenue uses `payment_orders WHERE status = 'paid'` after reconciliation.
  4. Recent QRIS/order list includes status, amount, checkout URL presence, provider reference, created/updated time, and credited status.
- Export the provider-status refresh helper from the payment route/service so admin summary can reuse the same reconciliation logic as `/orders/:id/status`.
- When a pending QRIS becomes paid, grant credits idempotently and set `credited_at`; revenue should increase immediately on next poll.
- Surface production mode from backend config (`mode`, `productionLive`) and verify public `/api/health` reports `live-production`, not just `ok: true`.

## Verification checklist
- `npm run build:server && npm run build:web`
- `NODE_ENV=test ... jest --runInBand tests/api`
- `bash scripts/deploy.sh`
- Public health: env is `live-production`.
- Public catalog smoke: enabled OpenAI count > 0, ModelArk/Seedance count > 0, sample Kimi ids present if provider lists them.
- Generation smoke: at least one known OpenAI text model succeeds. Test Kimi separately and classify 404 access errors as provider/account configuration.
- QRIS smoke: run bounded pending-order refresh in the app container and compare paid revenue before/after; never print provider secrets.
