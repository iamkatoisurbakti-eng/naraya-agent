---
name: ksr888-gamexaglobal-provider-sync
summary: Live sync notes for imported PHP hosts using GameXaGlobal as the single game provider API.
---

# KSR888 GameXaGlobal provider sync notes

## What this session established
- GameXaGlobal auth on the live docs app uses `POST /api/auth/login` with JSON body:
  - `agent_code`
  - `password`
- Provider listing uses `GET /api/games/providers` with a bearer token from login.
- The docs app assets revealed the client path `https://api.gamexaglobal.com`.

## Failure modes seen in practice
- `400 Invalid credentials` means the login body is wrong or the host is pointing at the wrong credentials/source.
- `401 Access token required` means the provider list request was made without a valid bearer token.
- If login fails, try the stored bearer token and the `GAME_LIBRARY_TOKEN` env token as fallback candidates without printing either value.
- If `/api/games/providers` still returns `403 Invalid token`, the backend wiring is ready but live GameXaGlobal sync is blocked by provider credentials; keep DB-backed frontend fallbacks active and update the DB/env token before rerunning sync.
- After installing a valid GameXaGlobal bearer token, Pragmatic does not use the local legacy `PR` provider code upstream. Live provider codes observed: `PRAGMATIPLAY_SLOT` for Pragmatic Play slots and `PRAGMATIC_LIVE_ASIA` for Pragmatic Live Asia. `/api/games/provider/PR` returns provider-not-found, so launch/sync code must map local `PR` rows by type/name to these upstream provider codes or store a remote-provider mapping.
- For the KSR888 admin Game Library, keep endpoint-doc panels for `/api/players`, `/api/transactions`, `/api/transactions/stats`, and `/api/transactions/turnover-by-player`; show snapshot status when available and local DB fallbacks from `users`/`tb_user` plus `transaksi`/`tb_transaksi` so the admin panel remains useful while provider tokens are invalid.
- For `/transactions-overview`, use GameXaGlobal directly rather than the old `fiver()` history flow: populate the player select from `/api/players`, fetch per-player rows via `/api/players/{playerId}/transactions`, and render global turnover rows from `/api/transactions/turnover-by-player` with a selected-player summary fallback when the provider returns an empty turnover list.
- Do not log expected GameXaGlobal auth/token failures as runtime errors during admin page render; surface the warning in the UI and keep Laravel logs reserved for unexpected exceptions. Use a fresh log window after deploy (`: > storage/logs/laravel.log`, run smoke requests, then tail logs) before declaring clean.

## Sync rules for imported PHP hosts
- Treat the database row as source of truth for the active GameXaGlobal config.
- Before syncing provider/game rows, verify auth succeeds against the live endpoint.
- When syncing providers:
  - upsert by the composite identity `provider_code + provider_type`, not `provider_code` alone; KSR888 has repeated provider codes across categories (for example slot/live/fishing/arcade variants), and code-only merging hides valid providers on category pages
  - persist `provider_image`, `banner`, and `mobile_banner`
  - preserve previous image fields as fallback when the API omits them
- When rendering category provider pages:
  - merge DB/API provider rows by `provider_code:provider_type`, not by code alone
  - avoid arbitrary category limits unless the user explicitly asks; `/hot` previously hid OT providers because it was limited to 10 rows
  - if a provider type has no standalone route (for example `CB`), deliberately map it into the closest route such as `/p2p` and include it in live verification
- When syncing games:
  - persist `game_image` when the column exists
  - build an in-memory provider map during the same sync run so games without their own image can fall back to the freshly fetched provider images, not only stale DB data
  - fall back in this order: game image → provider image → provider banner → provider mobile banner → existing DB image
  - store raw API image URLs in the database; let the model accessors/proxy layer rewrite remote URLs at render time so DB remains the source of truth
- Clear cached provider/game payloads after sync so the homepage and category pages pick up the new DB rows.

## Verification pattern
1. Read `gx_*` from the `api` table.
2. POST `/api/auth/login`.
3. If login succeeds, GET `/api/games/providers` and GET `/api/games`.
4. Upsert provider/game rows and images.
5. Restart the host-specific web container.
6. Probe the live page and confirm new providers render.
