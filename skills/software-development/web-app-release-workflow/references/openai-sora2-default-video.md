# OpenAI Sora 2 as default Video Studio model

Use this note when making OpenAI Sora 2 the default AI Video Generator model in the Nusantara AI SaaS-style React + Express app.

## Source changes
- Add a `video` catalog entry in `src/models/catalog.ts`:
  - `id: 'sora-2'`
  - `label: 'OpenAI Sora 2'`
  - `provider: 'openai'`
  - `envVar: 'OPENAI_API_KEY'`
- Sort video models in `src/routes/models.ts` so `sora-2` ranks first; `/api/models/catalog` and `/api/models/studio` should both return it as the first video model.
- Add per-model options in both backend catalog and frontend StudioPanel helpers:
  - durations: `[4, 8, 12]`
  - aspect ratios: `['16:9', '9:16', '1:1']`
- Keep UI ratio labels numeric only (`16:9`, `9:16`, `1:1`).
- Add backend duration coercion for Sora 2 so unsupported request durations snap to supported values.
- Add/adjust credit pricing in the shared credit helper; in the observed implementation `sora-2` used duration-priced video credits with 8s = 640 credits.

## Generate routing
- Treat Sora 2 as an OpenAI video model separately from GPT text models. Do not reuse the text-only GPT allowlist for video.
- Provider status for `video` should consider `OPENAI_API_KEY` configured, not only FAL/ModelArk keys.
- Keep secrets in env only. Verification may report `set/missing`, but never echo the actual key.
- If calling OpenAI video generation, isolate it in a dedicated helper such as `callOpenAiSoraVideo(prompt, model, { aspectRatio, duration, quality })` so media routing stays flat and mutually exclusive.

## Tests and smoke checks
- Extend model API tests to assert:
  - `sora-2` exists, provider `openai`, enabled when `OPENAI_API_KEY` is set
  - `supportedDurations` equals `[4, 8, 12]`
  - `aspectRatios` equals `['16:9', '9:16', '1:1']`
- Run:
  - `npm run typecheck`
  - relevant API tests, especially model catalog/studio tests
  - `npm run build:web`
  - `npm run build:server`
  - `npm run test:e2e`
- For browser smoke, seed `localStorage` with both access and refresh tokens; this app's bootstrap ignores sessions that lack `nusantara.refreshToken`.
- In Video Studio smoke tests, the first select is model, the second select is aspect ratio, and the third select is duration.
- Verify production with `/api/models/catalog`, `/api/models/studio`, `/api/generate/quote?capability=video&model=sora-2&duration=8`, mobile Chromium `390x844`, health, and `docker compose ps`.
- Avoid spending real provider credits unless the user explicitly requests a real generation smoke test.

## Cleanup
- Live smoke users should use deterministic disposable email patterns and be deleted from the production SQLite DB after verification, along with credit accounts, ledger rows, and refresh tokens.
