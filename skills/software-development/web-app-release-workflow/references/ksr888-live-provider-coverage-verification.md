# KSR888 live provider coverage verification

Use this note when the user asks to verify that all GameXaGlobal/KSR888 providers appear on `ksr888.online`.

## What this session found
- Active provider rows can share the same `provider_code` across different `provider_type` values.
- Treat provider identity as `provider_code:provider_type` for category rendering and sync merges.
- Code-only merge can hide valid variants such as fishing/live/poker/arcade entries.
- `/hot` must not be capped with an arbitrary `take(10)` when the task is “all providers”.
- `CB` had no standalone route; map it intentionally into `/p2p` unless a dedicated route is added.

## Verification pattern
1. Query active DB providers and group by type:
   - `SL` -> `/slots`
   - `LC` -> `/casino`
   - `SB` -> `/sports`
   - `PK` -> `/p2p`
   - `CB` -> `/p2p`
   - `FH` -> `/fishing`
   - `LK` -> `/lottery`
   - `OT` -> `/hot`
2. Fetch each live URL with a browser-like user-agent. Curl/default bot UA can get partial/mobile/script-only HTML.
3. Parse visible provider evidence from `<img alt="...">` and mobile `.g-title` nodes.
4. Compare every expected provider name for that type to the live HTML. Report `expected`, `missing_count`, and missing provider names.
5. If missing providers have duplicate codes, inspect controller merge keys before changing the database.

## Live success shape from this session
- Active DB providers: 55
- Breakdown: `SL=23`, `LC=8`, `SB=5`, `PK=4`, `CB=1`, `FH=8`, `LK=3`, `OT=3`
- Final verification: every mapped route had `missing_count=0`.

## Patch pattern that fixed it
- In `SgGameController::categoryProviders`, key `$providersByCode` by `$providerCode . ':' . $providerType`.
- In `GameController::syncGameXaGlobal`, upsert providers by `provider_code + provider_type`.
- Change `/hot` from `categoryProviders([], 10)` to `categoryProviders([])`.
- Include `CB` in `/p2p`: `categoryProviders(['PK', 'CB'])`.
