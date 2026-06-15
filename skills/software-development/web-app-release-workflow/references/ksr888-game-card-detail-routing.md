# KSR888 game/provider card detail routing

## Problem
Game cards and provider cards were linking to generic pages (for example `/slots`) or using mixed route logic in multiple Blade files. That made category navigation inconsistent across homepage rows and game lists.

## Fix pattern
- Add a model accessor:
  - `SgGame::getDetailUrlAttribute()` for game cards
  - `SgProvider::getDetailUrlAttribute()` for provider cards
- Map route targets from category/type once in the model:
  - `SL` → `/slots/server-a/{provider}`
  - `LC` → `/casino`
  - `SB` → `/sports`
  - `PK` → `/p2p`
  - `FH` → `/fishing`
  - `LK` → `/lottery`
  - `OT` → `/hot`
- In Blade, link cards with `{{ $item->detail_url }}` instead of inline route logic.
- Reuse the same accessor in:
  - homepage game rows
  - provider rows
  - game list/catalog cards

## Verification
- `php -l` on the touched model/controller files
- deploy
- `curl` the live homepage and confirm the rendered links contain the expected category routes
- if needed, inspect the live HTML for `href="https://.../slots/server-a/..."`, `/casino`, `/sports`, etc.

## Pitfalls
- Do not hardcode `/slots` for every card; that loses category context.
- If a view already uses a generic provider image fallback, keep only the `href` logic changing so appearance stays stable.
- When the app is served behind a proxy/CDN, verify the live HTML rather than assuming the source edit is live.
