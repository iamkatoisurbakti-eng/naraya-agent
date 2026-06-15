# KSR888 Game Launch Troubleshooting

Use this when a mobile click looks broken but the real problem may be upstream launch rejection.

## What we verified in-session
- Mobile game cards in `/slots/server-b/{provider}/{type}` can correctly render a launch anchor to `/game_process/{game_code}/{game_provider}`.
- `connect_games()` should be the authoritative launch route for `/game_process/{game_code}/{game_provider}`.
- A successful redirect chain may go:
  1. local `/game_process/...`
  2. `api.httpsgamexaglobal.net/api/games/proxy/...`
  3. provider domain / launch URL
- If the final chain works for one game, the mobile issue is likely selector/route specific, not global.

## Fast verification recipe
1. Pick one concrete active game row from `games`.
2. Call `connect_games()` or `providerLaunch()` with the exact route parameters.
3. Confirm the first 302 target.
4. Follow the redirect chain with `curl -I -L`.
5. If the chain ends at a provider launch URL, the route is healthy even if some other game/provider still fails.

## Common failure patterns
- `302` to `/slots` or `/masuk`: route or auth branch is blocking before launch.
- `404 Player not found in GameXaGlobal`: player sync issue, not a click issue.
- `10016 The account has been frozen`: upstream token/agent/account issue; changing frontend will not fix it.
- Browser auto-launch failures on shared hosts may be caused by Chromium profile singleton/socket conflicts; switch to terminal verification or a fresh user-data dir.

## Useful probes
- `curl -I -L https://ksr888.online/game_process/<game_code>/<provider>`
- controller-side probe via Laravel tinker / a small PHP script in the web container
- direct follow-up to the upstream proxy URL returned by `connect_games()`

## Notes
- Prefer verifying one specific active game end-to-end instead of probing many providers at once.
- If the route works for one game, keep frontend changes small and focus on the upstream game payload/provider mapping for failures.
