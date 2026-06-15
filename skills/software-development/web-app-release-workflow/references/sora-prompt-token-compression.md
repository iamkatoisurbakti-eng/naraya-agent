# Sora prompt/token compression for cost control

Use when OpenAI Sora video generation is expensive or prompts are bloated, but the product must keep Sora 2 as the default video model.

## Pattern
- Keep the user’s original prompt in generation history/response for transparency.
- Build a separate provider prompt for Sora only, immediately before the OpenAI call.
- Compact the provider prompt server-side:
  - normalize whitespace/newlines
  - remove provider/control noise (`OpenAI`, `Sora 2`, `model`, `provider`, `generate`, `tolong`, etc.)
  - collapse repeated style words such as `cinematic cinematic`, `realistic realistic`, `ultra ultra`
  - trim to a hard provider-safe limit (about 900 chars for base text, about 1050 chars after compact suffix)
  - append only essential options: duration seconds, numeric ratio, quality, natural motion, coherent subject, clean composition
- Do not add verbose generic “video options” prompt text for Sora; provider JSON fields already carry `seconds`, `size`, and `quality`.
- Preserve normal credit pricing by duration; compression should reduce provider prompt tokens, not silently discount customer credit unless business rules change.

## Test shape
- Mock `global.fetch` for the OpenAI video call.
- Submit a deliberately long/repetitive prompt to `/api/generate` with `capability: video`, `model: sora-2`.
- Assert:
  - response provider remains `openai`
  - stored response/history prompt equals the original truncated user prompt
  - request body sent to OpenAI has `model: sora-2`, correct `seconds`, correct numeric `size`
  - provider prompt length is below the limit and less than half the original prompt
  - provider/control noise and repeated words are absent

## Live verification without spending video credits
- Do not run a real Sora video generation unless the user explicitly permits paid usage.
- Verify instead:
  - `/api/health` OK
  - `/api/models/studio` still returns video default `sora-2` / provider `openai`
  - `/api/generate/quote?capability=video&model=sora-2&duration=4` returns expected credit cost
  - deployed container JS contains the compression helper (for this repo path: `/app/dist/src/routes/generate.js`)
- If a temporary production user is created to call quote endpoints, remove matching test users plus credit accounts, ledger rows, refresh tokens, and generation history afterward.

## Nusantara AI repo specifics
- Source: `/root/nusantara-ai-saas/src/routes/generate.ts`
- Regression test: `/root/nusantara-ai-saas/tests/api/generate-provider.test.ts`
- The built route file inside the container is `/app/dist/src/routes/generate.js`, not `/app/dist/routes/generate.js`.
- Back up changed source/tests outside the project root before deploy, for example `/root/nusantara-ai-saas-backups/sora-token-compression-YYYYMMDD-HHMMSS`.
