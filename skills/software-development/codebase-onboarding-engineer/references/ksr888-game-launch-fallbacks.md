# KSR888 Game Launch Fallbacks

Scope: KSR888 Laravel game launch troubleshooting where the UI renders but the user gets `Game belum bisa dibuka. Silakan coba lagi.` or a GameXaGlobal launch rejection.

Key lessons from the mobile launch fix:
- If `fiver->opengame()` returns a rejection, try both parameter orders before declaring failure:
  1. `opengame($playerName, $providerCode, $gameCode)`
  2. `opengame($playerName, $gameCode, $providerCode)`
- Some GameXaGlobal-compatible launch endpoints accept a URL even when the status field is not the expected success value. Treat a non-empty HTTP URL as a valid launch result when the response is otherwise structured like a launch response.
- When building GameXaGlobal launch payloads, include compatibility aliases in addition to the documented fields:
  - `player_id`
  - `player_name`
  - `game_uid`
  - `provider_code`
  - `game_type`
  - `lang`
  - `currency`
  - `lobby_url`
  - plus aliases like `game_code`, `game_id`, `game`, `provider`, `type`
- If the old error persists, inspect the live container copy and restart before retesting the mobile URL.

Live-verification notes:
- Use a mobile user-agent curl against the nested slot route.
- Confirm the route returns HTTP 200 before debugging provider launch payloads.
- If launch still fails, capture provider code, game code, and the exact URL before changing more code.
