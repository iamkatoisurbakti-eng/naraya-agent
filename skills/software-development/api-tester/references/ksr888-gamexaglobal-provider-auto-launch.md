# KSR888 GameXaGlobal Provider Auto-Launch

## Context
KSR888 provider cards used local provider codes and legacy game codes, while GameXaGlobal launch requires upstream provider codes and upstream game hash IDs.

Example mismatch:
- Local provider `PR`
- Local game codes such as `vs20olympgold`, `vswayslions`
- GameXaGlobal provider `PRAGMATIPLAY_SLOT`
- GameXaGlobal game codes are hash-like IDs such as `b066c2bdef0f2d541a2317ed5fdac3b4`

If the local code is sent directly to `/api/games/launch`, GameXaGlobal returns errors like `Game not found or inactive`.

## Proven fix pattern
1. Keep provider cards clickable, but remove visible provider CTA buttons if requested.
2. Change provider card target from category/list pages to an auto-launch route:
   - from `/slots/server-b/{provider}/{type}`
   - to `/provider-launch/{provider}/{type}`
3. In the provider launch route:
   - require login; unauthenticated users redirect to `/masuk`
   - select an active local game for that provider/type, preferably well-known playable names first
   - redirect to `/game_process/{game_code}/{provider}`
4. In `connect_games` / launch flow:
   - if local code/provider is legacy, map provider aliases and resolve the upstream GameXaGlobal game via the live catalog before launching
   - match by exact normalized game name first, then loose contains match if needed
   - cache the GameXaGlobal launch catalog briefly (`Cache::remember`) to avoid a remote catalog fetch for every click
5. Launch against `/api/games/launch` only after resolving:
   - upstream provider code
   - upstream game hash/id
   - real provider player id

## Provider aliases observed
Useful aliases for KSR888 local provider codes:
- `PR` -> `PRAGMATIPLAY_SLOT`, `PRAGMATIC_LIVE_ASIA`
- `PG` -> `PGSOFT_SLOT`
- `HB` -> `HABANERO_SLOT`
- `CQ` -> `CQ9_SLOT`
- `JA` -> `JILI_GAMING`
- `JD` -> `JDB_GAMING`
- `MP` -> `MICORGAMING_SLOT`
- `PN` -> `PLAYNGO`
- `YD` -> `YGR`
- `EP` -> `EVOPLAY`
- `BG` -> `BNG`, `BOOONGO`
- `P2` -> `SKYWIND`
- `SG` -> `SPADE_GAMING`
- `5G` -> `5G`
- `BT` -> `BTGAMING`, `BIG_TIME_GAMING`

## Verification recipe
Inside the `ksr888-web` container, Laravel CLI probes may need a PTY or `script -qec` because non-TTY PHP can throw Symfony `StreamOutput` errors.

Verify provider page HTML:
- `/slots` contains `/provider-launch/`
- `/slots` no longer contains `/server-b/` for provider cards
- requested provider buttons/CTA strings are absent (`btn-hvrplay`, `provider-play-now-btn`, `MAIN SEKARANG`)

Verify unauthenticated behavior:
- `GET /provider-launch/PR/SL` returns `302` to `/masuk`

Verify authenticated behavior with a known test user:
- `/provider-launch/PR/SL` returns `302` to `/game_process/{game_code}/PR`
- `/game_process/{game_code}/PR` returns `302` to a GameXaGlobal launch URL (host observed: `api.gamexaglobal.com`)

## Pitfalls
- Do not expose provider tokens or env values in output.
- Do not assume local provider codes equal GameXaGlobal provider codes.
- Do not assume local Pragmatic game slugs are valid upstream launch IDs.
- Avoid forcing all provider clicks to a single static game; select an active game for that provider/type so every provider session has a launch path.
- Removing provider buttons should not remove the anchor around the card; card clickability must remain.
