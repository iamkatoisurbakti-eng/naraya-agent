# Dashboard generation history + real visitor metrics

Session-derived pattern for Dockerized React + Express + SQLite dashboards where generated media/history and visitor counts must be live and production-backed.

## Problem signals
- User can generate successfully, but dashboard history is empty.
- Total generate card does not increase after generations by any user.
- Visitor card shows fake/static numbers instead of real `nusantara-ai.online` traffic.

## Backend source of truth
- Use `generation_history` as the source of truth for generate dashboard stats/history, not stale `usage_metrics` or demo `projects` rows.
- Keep per-user privacy for history:
  - `WHERE user_id = ? AND expires_at >= CURRENT_TIMESTAMP`
  - `ORDER BY created_at DESC`
  - bounded `LIMIT 30` for dashboard display
- Global totals can aggregate all users:
  - `SELECT COUNT(*) FROM generation_history` for global total generate.
- Keep compatibility with old tests/demo metrics if needed by using a fallback only when the `generation_history` count is zero.

## Frontend dashboard live update
- Convert summary fetch to a reusable `loadSummary` callback.
- Refresh immediately after own generation via `StudioPanel` callback such as `onGenerated?.()`.
- Poll dashboard summary while the dashboard/history section is active; 5 seconds is a good default.
- Render history cards from real `result.url`/`result.text` when available; avoid placeholder images for generated history.
- If the user asks users to “tetap bisa melihat generate yang sudah berlalu,” add a dedicated sidebar/menu section (for example `History Generate`) instead of only a small recent-projects strip on the dashboard.
- Type the dashboard summary to include `generationHistory` separately from `recentProjects`; use `recentProjects` for compact dashboard cards and `generationHistory` for the full 30-day user history page.
- The full history page should support all capabilities:
  - image/video: preview `result.url`, using `<video controls>` for video
  - audio/voice: play `result.audioBase64` with a data URL and `mimeType`
  - text/chat: show `result.text` in a readable text preview
  - show prompt, provider, model, credit cost, `createdAt`, `expiresAt`, and download/open link when a URL exists

## Visitor tracking pattern
- Track server-side before static SPA fallback so public page visits are counted even before login.
- Use a long-lived HTTP-only cookie (for example `nusantara_vid`) as `visitor_key`.
- Hash IP/remote address if stored; do not display raw IPs.
- Add `app.set('trust proxy', 1)` behind Caddy/Compose so Express has usable client/proxy data.
- Insert visitor events best-effort only; analytics must never block page loads.
- Add/maintain SQLite fields:
  - `visitor_key`, `path`, `referer`, `user_agent`, `ip_hash`, `host`, `created_at`
  - `addColumnIfMissing(..., 'visitor_events', 'host', 'TEXT')` for existing DBs
- Count “real visitor” by excluding obvious bots/crawlers/spiders in SQL/user-agent filtering.
- Return both unique visitors and page views:
  - today unique visitors
  - today page views
  - total unique visitors
  - total page views

## Verification
- Run `npm run build:server`, `npm run build:web`, and relevant API tests.
- Deploy with the project deploy script.
- Hit the public homepage with a browser-like user-agent, then query dashboard summary/admin summary.
- For 30-day generation history, run an authenticated smoke generate, then verify `/api/dashboard/summary` returns `summary.generationHistory[0]` with `result`, `createdAt`, and `expiresAt`; check `expiresAt - createdAt` is about 30 days.
- Clean up deterministic live smoke users and their related `generation_history`, `credit_ledger`, and `credit_accounts` rows after verification.
- Verify public health and inspect runtime dist in the container if stale code is suspected:
  - `docker compose exec -T app node -e "import('/app/dist/src/services/dashboard-service.js').then(m=>console.log(m.getDashboardSummary.toString().includes('totalGenerations')))"`

## Pitfalls
- Video providers such as ModelArk/Seedance can finish after 60+ seconds; do not save a final video history row while `rawStatus` is still `running` unless there is a follow-up refresh path. Poll long enough for normal completion and save `result.url` only after `succeeded`.
- Provider-hosted generated video URLs can fail preview later due expiry/CORS/range handling. Mirror successful generated image/video outputs to `data/generate-assets/<generationId>/output.<ext>` and expose them through `/generated-media/...` so browser preview and download work reliably from history.
- A successful local build can still leave stale runtime behavior if the deployed container is not rebuilt/recreated; inspect `/app/dist/...` inside the container.
- Docker build context may copy source that changed after a prior build; rerun deploy after final patches.
- Existing `visitor_events` rows may have `host` null until the new column is deployed; totals should not depend only on `host = 'nusantara-ai.online'` unless backfilled.
- The authenticated user dashboard should not expose other users' prompts/results; only global aggregate counts should cross user boundaries.
