# Dynamic model credit pricing and chat UI

Use this reference when a credit-metered AI studio has a model selector and the visible generate/send price does not change when the user switches models.

## Pattern
- Treat backend pricing as the source of truth. Add/extend a helper like `creditCostForGeneration(capability, model, options)` and use it in the actual `/api/generate` charge path, not only in UI constants.
- Expose the same computed price on model endpoints and/or quote endpoints:
  - `/api/models/catalog`: include baseline `creditCost` on every model.
  - `/api/models/studio`: include baseline `creditCost` on every grouped studio model.
  - `/api/generate/quote`: return the live quote by `capability + model` and any price-affecting options such as video `duration`.
- Update frontend model types to include `creditCost`.
- In the studio component derive the selected baseline price from `availableModels.find(m => m.id === model)?.creditCost`, falling back to capability defaults only when no model exists; if an option can change price, call the quote endpoint and render that live quote instead.
- Render the dynamic price in all user-facing places:
  - model dropdown option text
  - generate/send button label
  - explanatory credit note near the button
  - result/history row if relevant
- Backend `/api/generate` must consume the exact same helper with the selected `model` and price-affecting options so UI and ledger cannot drift.

## Option-dependent video pricing
When the user reports that changing Seedance/video duration does not change credit price:
- Extend the pricing helper to accept duration, e.g. `creditCostForGeneration(capability, model, duration)`.
- In `/api/generate/quote`, read `duration` from query params, validate/coerce it with the same selected-model duration helper used by generate, and return the resulting credit cost.
- In `/api/generate`, compute `durationSeconds` once from the request body, pass it to the pricing helper, and send that same coerced duration to the provider payload.
- In the React studio quote `useEffect`, append `duration` to the quote query when `active === 'video'` and include `duration` in the dependency array so the displayed button/help-text credit updates immediately when the dropdown changes.
- A simple proportional Seedance pattern is to treat the configured 5-second price as base and return `ceil(baseCost * seconds / 5)`, after coercing duration to a supported value. Verify both quote and actual ledger use the same number; do not run paid generate smoke tests unless the user explicitly approves cost.

## Tests to update
- If model API snapshots/exact equality tests exist, update expected grouped/catalog objects to include `creditCost`.
- If a provider routing test asserts credit balance deltas, keep compatibility aliases stable. Example: if `seedance-2` is a friendly alias previously charged at 250 credits, preserve that unless the business rule explicitly changes it; charge the underlying live ModelArk id separately if needed.
- Run full API tests after frontend/build because response shape changes can fail exact tests.

## Chat UI release pattern
When the user asks for ChatGPT-like chat in an existing studio panel:
- Keep model selector + credit price visible in the composer.
- Add a left history sidebar with `New Chat` and session titles.
- Use a wide center chatbox with user/assistant bubbles.
- Add a right result/response panel for the latest answer/model/provider/credit metadata.
- If server-side token streaming is not implemented yet, add a lightweight typing/streaming effect after the response arrives, but do not claim true SSE/WebSocket streaming.

## Production verification
- Build server and web.
- Run API tests.
- Deploy through the project script.
- Verify public endpoints return `creditCost` for every catalog/studio model.
- For Vite SPAs, grep the served production JS bundle for new UI copy/markers (for example `Panel Respons`, `AI sedang mengetik`, `kredit / pesan`) because homepage HTML only proves the shell loaded.

## Pitfalls
- Do not hardcode pricing only in React constants; this creates mismatched button prices and actual credit deductions.
- Do not add fields to API response objects without updating exact tests.
- Do not use static capability pricing for all text/video models if provider cost varies significantly by model.
- Dynamic provider catalog loading should still be disabled under `NODE_ENV=test` when tests expect deterministic catalog lengths.
