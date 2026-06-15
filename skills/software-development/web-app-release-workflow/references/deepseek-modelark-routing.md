# DeepSeek via BytePlus ModelArk Routing Notes

Nusantara AI SaaS production pattern for enabling DeepSeek from BytePlus/ModelArk.

## Discovery
- Query ModelArk dynamically with:
  - `GET ${ARK_BASE_URL:-https://ark.ap-southeast.bytepluses.com/api/v3}/models`
  - auth header `Authorization: Bearer $ARK_API_KEY` (or aliases `BYTEDANCE_API_KEY` / `BYTEPLUS_API_KEY`).
- DeepSeek models may appear with mixed statuses. In the observed production account:
  - `deepseek-v3-2-251201` was callable and should be the active target.
  - older ids such as `deepseek-r1-250120`, `deepseek-v3-241226`, `deepseek-v3`, etc. were `Shutdown`.
  - retiring ids such as `deepseek-r1-250528` and `deepseek-v3-1-250821` were listed but `/responses` returned `InvalidEndpointOrModel.NotFound` for this account.

## Routing fix
- Keep the customer-friendly alias `deepseek`, but map it server-side to the active ModelArk id:
  - `deepseek` -> `deepseek-v3-2-251201`.
- Treat `deepseek-*` ids as ModelArk text models in `/api/generate` before OpenAI fallback.
- Set catalog entries to use `provider: 'deepseek'` and `envVar: 'ARK_API_KEY'`, not `DEEPSEEK_API_KEY`, when the integration is through BytePlus.
- Dynamic ModelArk catalog should classify ids starting `deepseek-` as provider `deepseek`.
- Filter both `Shutdown` and `Retiring` ModelArk models from the public dynamic catalog so users do not select models that are listed but fail at generation.

## Verification
- Direct smoke test `/responses` against `deepseek-v3-2-251201` before exposing it.
- Production smoke through app:
  1. Register/login a temporary user.
  2. POST `/api/generate` with `{ capability: 'text', model: 'deepseek', prompt: '...' }`.
  3. Expect status `200`, result provider `byteplus-modelark`, and result model `deepseek-v3-2-251201`.
- Do not print provider keys; report only masked env status, model ids, status codes, and response length.
