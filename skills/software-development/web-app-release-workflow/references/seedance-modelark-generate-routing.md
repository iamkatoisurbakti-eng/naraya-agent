# Seedance / ModelArk generate routing fix

Use this when Seedance video generation appears broken in Nusantara AI SaaS.

Symptoms seen:
- `src/routes/generate.ts` fails Jest/TypeScript with errors near the `catch` of `/api/generate` (`TS1005: 'try' expected`, `TS1472: 'catch' or 'finally' expected`).
- `/api/generate/status` reports video studio disabled even when `ARK_API_KEY` is configured.
- Seedance video risks falling back to FAL instead of BytePlus ModelArk.

Root causes found:
- A duplicated/nested `else if (capability === 'image' || capability === 'video')` block corrupted the generate route and accidentally swallowed the audio branch.
- `callArk()` referenced `apiKey` without declaring it and used `config.arkApiKey` directly, so runtime aliases (`BYTEDANCE_API_KEY`, `BYTEPLUS_API_KEY`) and late env reads were not consistently honored.
- `/api/generate/status` only considered FAL for image/video studios; ModelArk-backed Seedance/Seedream should also make those studios available.

Known-good pattern:
- Keep a single media branch:
  - `video && isSeedanceModel(model)` -> `callArkSeedanceVideo(...)`
  - `image && isSeedreamModel(model)` -> `callArkImage(...)`
  - FAL/Flux models -> `callFal(...)`
  - if still no result, throw provider-specific `PROVIDER_NOT_CONFIGURED`
- Keep `audio` as its own sibling branch after image/video:
  - `else if (capability === 'audio') result = await callElevenLabs(...)`
- In ModelArk calls, read keys through `arkApiKey()` and base URL through `arkBaseUrl()`.
- In `/api/generate/status`, mark `studios.image` and `studios.video` true if either FAL keys OR `arkApiKey()` are set.

Regression test pattern:
- Mock `global.fetch` for Seedance task create + poll success.
- Send `/api/generate` with `{ capability: 'video', model: 'seedance-2', ... }`.
- Assert provider is `byteplus-modelark`, URL comes from ModelArk response, FAL URL is not called, and credits are charged only after success.

Verification commands:
- `npx cross-env NODE_ENV=test DATABASE_FILE=/tmp/nusantara-ai-test.db JWT_SECRET=test-secret jest --config jest.config.cjs --runInBand tests/api/generate-provider.test.ts`
- `npx cross-env NODE_ENV=test DATABASE_FILE=/tmp/nusantara-ai-test.db JWT_SECRET=test-secret jest --config jest.config.cjs --runInBand tests/api`
- `npm run build:server`
- `npm run build:web`

Production smoke:
- Use a temporary account, call `/api/generate/status` with bearer token, and verify `{ studios.video: true, providers.modelark: true }`.
- Do not print or echo actual API key values; only report masked `KEY=set/missing`.
