# Video Generation Preview + ModelArk Alias Notes

Session-specific notes from Nusantara AI SaaS production fixes.

## Stable generated video preview/download
- Provider-hosted video URLs can fail in browser preview or later history because of expiry, CORS, or byte-range behavior.
- After a video/image provider returns a successful HTTP URL, mirror the asset server-side into `data/generate-assets/<generationId>/output.<ext>` and expose it through the app static route `/generated-media/<generationId>/output.<ext>`.
- Save the mirrored URL in `generation_history.result_json.url` and keep the provider URL as `remoteUrl` for backup/debug only.
- Use `fetch(url, { signal: AbortSignal.timeout(120000) })` around mirroring and return the original result on mirror failure so a successful generation is not lost.
- UI should render video results with:
  - `<video controls preload="metadata" playsInline ...>`
  - a separate `Download Hasil` link with `download`
  - a separate `Buka Preview` link with `target="_blank"`
- History UI should render the same video player/buttons from parsed `result_json`; if no URL is available but `kind === 'video'`, show a clear “preview belum siap” message instead of silently showing only text/status.
- If older rows have `taskId` and `rawStatus: running`, a one-off backfill can query ModelArk task status, mirror `content.video_url`, and update `generation_history.result_json`.

## Seedance polling and durations
- Do not save final video history while ModelArk/Seedance is still `running` unless there is an async refresh path. Increase polling for normal completion before inserting the final history row.
- Seedance production duration mapping used here:
  - `seedance-2` / `dreamina-seedance-2`: `[3, 5, 10, 15]`
  - `seedance-1.5` / `seedance-1.0 pro`: `[5, 10, 15]`
  - `seedance lite-i2v`: `[5]`
- Keep frontend catalog metadata, frontend fallback, and backend duration coercion in sync.

## ModelArk friendly aliases
- Friendly UI aliases must be mapped to callable ModelArk ids before `/responses` calls. Do not send the alias if provider does not accept it.
- Known mappings from this session:
  - `deepseek` -> `deepseek-v3-2-251201`
  - `kimi-k2` -> `kimi-k2-250905` (catalog only if provider/account access still returns `InvalidEndpointOrModel.NotFound`)
  - `dola-seed-2-0` -> `seed-2-0-pro-260328`
  - `dola-seed-2-0-mini` -> `seed-2-0-mini-260215`
  - `dola-seed-2-0-lite` -> `seed-2-0-lite-260228`
  - `bytedance-seed-1-6` -> `seed-1-6-250915`
- Smoke test real generation endpoints separately from catalog visibility. In this session, Mini/Lite/Seed 1.6/DeepSeek V3.2 succeeded; Kimi K2 appeared in catalog but failed with ModelArk account/endpoint access (`InvalidEndpointOrModel.NotFound`).

## Verification pattern
- Build: `npm run build:server && npm run build:web`
- Tests: `npx cross-env NODE_ENV=test DATABASE_FILE=/tmp/nusantara-ai-test.db JWT_SECRET=[REDACTED] jest --config jest.config.cjs --runInBand tests/api`
- Deploy: `bash scripts/deploy.sh`
- Public checks:
  - `/api/health` reports `live-production`
  - `/api/models/catalog` contains requested model labels/ids and `enabled: true`
  - a mirrored video URL under `/generated-media/...` returns `HTTP 200`, `content-type: video/mp4`, and `accept-ranges: bytes`
