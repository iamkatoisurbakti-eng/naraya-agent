# Free Chat AI model pricing and ordering

Use when a Nusantara-style credit-metered app needs selected chat models to be free for all users while other studios remain credit-gated.

## Pattern
- Put the free-model rule in the shared backend pricing helper, not only in frontend labels. In this repo that is `creditCostForGeneration(capability, model)` in `src/services/credit-service.ts`.
- Add an explicit helper such as `isFreeChatModel(model)` and normalize ids by lowercasing and replacing non-alphanumerics with `-` so friendly spellings like `DeepseekV3.2`, `Dola-seed2.0lite`, and provider ids can map to the same rule.
- Return `0` only for `capability === 'text'` and the approved model ids/aliases. Do not make media/video variants free by substring accident.
- Keep `/api/generate/quote`, `/api/models/catalog`, `/api/models/studio`, and `/api/generate` all using the same helper so visible price, quote, and ledger charge cannot drift.
- `consumeCredits()` should already no-op for amount `0`; verify it returns without adding a debit ledger row and the user's balance remains unchanged after a successful free generation.

## UI behavior
- In the model selector, render `Gratis` instead of `0 kredit` for `creditCost === 0`.
- Sort free Chat AI models to the top of the text model list on the backend catalog/studio endpoints. Keep test determinism by bypassing backend UI sorting under `NODE_ENV=test` if existing API tests assert exact static catalog/provider order.
- Also sort/default in the frontend studio component, not only the backend. If the dashboard passes `/api/models/catalog` directly into a model selector, use a memoized scoped model list for Chat AI and set the selected model to the first enabled free model whenever the active studio/model list changes. This prevents stale/default paid models if catalog ordering or async loading changes.
- Use an explicit rank function for business-priority free models rather than a generic `creditCost === 0` sort. Dynamic provider ids (for example raw `seed-2-0-mini-*` / `seed-2-0-lite-*` or friendly aliases like `deepseek`) may also be free, but should not interleave ahead of the requested top models.
- Suggested top order from this session:
  1. Kimi K2
  2. Dola-Seed-2.0 Mini
  3. Dola-Seed-2.0 Lite
  4. DeepSeek V3.2
  5. other free aliases/dynamic ids, if exposed

## ModelArk routing caveat
- Friendly UI ids can be free and visible, but provider generation still needs a callable real ModelArk id. Map aliases server-side before calling `/chat/completions`.
- Smoke-test actual generation for each provider route. ModelArk can list Kimi ids while the account endpoint still returns `InvalidEndpointOrModel.NotFound`; report that as provider/account access rather than a pricing bug.

## Verification checklist
- Build server and web.
- Run API tests with `NODE_ENV=test` and a dummy `JWT_SECRET`.
- Deploy via `bash scripts/deploy.sh`.
- Public catalog smoke: first text models include the free models and each has `creditCost: 0`.
- Authenticated quote smoke for every free id returns `0`.
- Authenticated generate smoke with a known callable free model returns status 200, generation `creditCost: 0`, and unchanged credit balance.
- Clean up temporary smoke users from production DB after verification.
