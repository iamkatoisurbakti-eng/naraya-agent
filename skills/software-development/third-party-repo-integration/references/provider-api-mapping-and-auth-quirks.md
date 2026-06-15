# Provider API Mapping and Auth Quirks

Session notes for mapping a third-party game provider API into the KSR888 host app.

## What was learned

- The provider credentials lived in the `api` table under legacy `sgx_*` columns:
  - `sgx_agent_code`
  - `sgx_token`
  - `sgx_endpoint`
  - `sgx_status`
- The newer `gx_*` columns were empty during the session, so the integration had to support both naming schemes to avoid breaking older admin screens.
- The live provider did **not** accept a static bearer token directly for every endpoint.
- `GET /api/auth/me` with the stored token returned `403 Invalid token`.
- `POST /api/auth/login` with `agent_code + password` returned `400 Invalid credentials` when the stored secret was wrong.
- The correct integration pattern is:
  1. read configured agent/secret from DB/env
  2. try login to obtain a runtime bearer token
  3. call `me`, `providers`, `games`, etc. with the returned token
  4. catch connection/auth exceptions so the page keeps rendering

## Practical mapping

- Settings form: mirror writes into both `sgx_*` and `gx_*` fields if the host still has legacy screens.
- Game Library page: cache the provider response briefly; do not block first render on remote calls.
- Admin balance card: use `/api/auth/me` as the summary source.
- Sync endpoint: keep DB sync idempotent and update `providers` / `games` from the provider response.

## Pitfalls

- Direct bearer token probes can fail even when the login flow is correct.
- Remote DNS or credential failures should return a graceful card warning, not a fatal page error.
- Do not assume provider tables use the same column names in every environment; inspect the live schema before writing update code.
- Avoid changing the UI layout just to surface provider state; keep the existing panel and add small status text/cards only.
