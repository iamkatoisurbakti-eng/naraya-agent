# GPT-only free Chat AI release pattern

Use when the business rule is: Chat AI should use GPT models only and be free.

## Implementation notes
- Backend allowlist should be explicit, not a fuzzy provider/model-label check.
  - Accept GPT family ids such as `gpt-3...`, `gpt-4...`, `gpt-5...`.
  - Reject misleading non-OpenAI ids that start with `gpt-` but are not OpenAI GPT chat models, for example `gpt-oss-*` from BytePlus/other providers.
- Keep the allowlist in the credit/pricing helper so catalog, quote, generate, subscription gating, and tests share the same rule.
- For public model catalog and studio endpoints:
  - filter text models to allowed GPT/OpenAI entries only
  - set `creditCost: 0`
  - keep `enabled` tied to `OPENAI_API_KEY`/OpenAI runtime availability
- For generation routes:
  - reject non-allowed text models before provider routing
  - route text generation directly to OpenAI for allowed GPT ids
  - make quote return `creditCost: 0` and `requiresSubscription: false`
- For UI copy:
  - use customer-facing labels like `GPT Chat Gratis`
  - Free plan copy should say `Unlimited Chat AI dengan model GPT gratis`

## Verification
1. `npm run typecheck`
2. `npm run test:api`
3. `npm run test:e2e`
4. Local or live endpoint probe:
   - `GET /api/models/catalog`: every `capability=text` model is OpenAI GPT and `creditCost === 0`
   - `GET /api/models/studio`: text studio models match the same rule
   - `GET /api/generate/quote?capability=text&model=<gpt-model>` returns `creditCost: 0` and `requiresSubscription: false`
   - a non-GPT text model quote/generate returns 400
5. After deploy: `curl /api/health`, `docker compose ps`, then repeat catalog/studio probes against the HTTPS domain.

## Pitfalls observed
- Backups placed inside the project tree can be picked up by Jest when they contain copied `tests/` files. Store release backups outside the project root (for example `/root/nusantara-ai-saas-backups/...`) or ensure backups do not include test files under discoverable paths.
- Playwright can flake on slow form fills even after the locator resolves. If the e2e flow is otherwise valid, use a project-level timeout such as `timeout: 60000` in `playwright.config.ts` rather than retrying deploy blindly.
- A naive `id.startsWith('gpt-')` allowlist can accidentally expose `gpt-oss-*`; prefer a stricter OpenAI GPT family regex plus provider check in catalog filters.
