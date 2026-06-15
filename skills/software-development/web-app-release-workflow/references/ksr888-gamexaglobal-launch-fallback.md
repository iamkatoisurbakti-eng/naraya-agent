# KSR888 GameXaGlobal launch fallback

Use this pattern when a KSR888 launch route needs to open a GameXaGlobal game but the local `games` table does not have a matching row yet.

## Observed issue
- `connect_games()` could return "Game tidak ditemukan" even though the remote GameXaGlobal catalog had the game.
- The launch flow already had `launchGameXaGlobal()`, but it was only reachable after a local DB hit.

## Fix pattern
1. Keep the local DB lookup first for speed and compatibility.
2. If local lookup misses, query the remote GameXaGlobal catalog by `provider_code` and `game_code`.
3. If a remote match is found, build a lightweight game object and pass it to `launchGameXaGlobal()`.
4. Only fall back to "game not found" after both local and remote lookups fail.

## Implementation notes
- Reuse the cached remote catalog key if present: `gamexaglobal:launch-games:v2`.
- Return a minimal object with at least:
  - `game_provider`
  - `game_code`
  - `game_name`
  - `game_type`
  - `game_category`
  - `game_api = 'gamexaglobal'`
- Keep logging specific so failures distinguish:
  - local-miss
  - remote lookup miss
  - remote launch rejected

## Verification
- Test a provider/game pair that exists only in the remote catalog.
- Confirm it redirects to the remote launch URL.
- Confirm local-only games still launch through the normal path.
- Confirm the user-facing error only appears after both lookups fail.
