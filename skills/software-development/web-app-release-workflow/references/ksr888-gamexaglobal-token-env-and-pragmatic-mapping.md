# KSR888 GameXaGlobal token/env and Pragmatic mapping

Session learning for KSR888/GameXaGlobal production work.

## Token and env handling
- Do not hardcode `GAME_LIBRARY_TOKEN` or `GAME_LIBRARY_AGENT_CODE` defaults in `docker-compose.yml`; keep them in `.env.production` / `.env` and pass through with `${VAR:-}`.
- If the user provides a bearer JWT, store it in the DB `api.gx_token` or secure env without echoing it in final output. If a plain `AG...` agent code is provided, store it as `GAME_LIBRARY_AGENT_CODE` in env and sync `api.gx_agent_code` from env.
- After env changes for `ksr888-web`, recreate the container with production env loaded:
  ```sh
  set -a
  [ -f .env.production ] && . ./.env.production
  [ -f .env ] && . ./.env
  set +a
  docker compose up -d --force-recreate ksr888-web
  ```
- Verify only masked status inside the container, e.g. `GAME_LIBRARY_AGENT_CODE=set`, `GAME_LIBRARY_TOKEN=missing/set`; never print token values.

## Pragmatic provider mapping
GameXaGlobal upstream provider codes can differ from local KSR888 codes.
- Local DB uses `PR` for Pragmatic rows.
- GameXaGlobal provider list returned:
  - `PRAGMATIPLAY_SLOT` = Pragmatic Play slot games
  - `PRAGMATIC_LIVE_ASIA` = Pragmatic Live Asia
- `/api/games/provider/PR` returns `404 Provider not found`; do not use local `PR` directly for upstream provider-game fetches or launch.
- Future launch/sync logic should map:
  - local `PR` + type `SL` -> upstream `PRAGMATIPLAY_SLOT`
  - local `PR` + type `LC` -> upstream `PRAGMATIC_LIVE_ASIA`
- API payloads observed for these endpoints returned game id/name but no image fields, so keep DB-backed image fallback/proxy logic active.

## Verification pattern
- Probe `/api/auth/me`, `/api/games/providers`, and then `/api/games/provider/<remote_code>`.
- Treat `403 Invalid token` as credentials issue; treat `404 Provider not found` on a local code as provider-code mapping issue.
- Keep all output masked/redacted in chat summaries.
