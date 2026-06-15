# KSR888 GameXaGlobal provider-list and launch consistency

Use this reference when the front-end provider list, provider tiles, or play buttons must stay aligned with the GameXaGlobal API.

## What changed in this session
- Front provider listings were switched to GameXaGlobal-only sources in `HomeController` and `SgGameController`.
- Provider cards/views were kept on `detail_url` so the same provider tile can open the GameXaGlobal launch route.
- `GameController::connect_games()` now has a remote GameXaGlobal fallback when a local `games` row is missing.
- Cache keys were versioned to avoid stale provider catalogs surviving the migration.

## Implementation pattern
- Use `gamexaglobal()->providers()` as the source of truth for provider presence on the front.
- Build a provider collection keyed by `provider_code`, and expose a `detail_url` attribute that points to the launch route.
- Keep the card/grid and play-button paths aligned to the same provider/game lookup path.
- When a local game is missing, look up the remote GameXaGlobal game by `provider_code` + `game_code` before failing the request.
- Prefer a fallback icon only for missing provider images; do not fall back to inactive or unrelated local providers.

## UI consistency notes
- Provider tiles should render the remote provider image/logo from GameXaGlobal-backed model accessors where possible.
- If a view shows a provider logo next to a game, use the same provider map as the provider list so the tile and launch path do not drift.
- For KSR888, keep the front provider list limited to providers returned by the API, not the legacy `providers` table.

## Pitfalls
- Do not cache the old provider list indefinitely; add a new cache version when the provider source changes.
- Do not keep hardcoded provider cards in Blade when the front is meant to reflect remote availability.
- Do not leave play buttons pointing at the legacy flow if the launch controller already has a GameXaGlobal path.
- If the container is rebuilt from copied source, remember that edits under `site/` require a rebuild/recreate before the live site changes.
