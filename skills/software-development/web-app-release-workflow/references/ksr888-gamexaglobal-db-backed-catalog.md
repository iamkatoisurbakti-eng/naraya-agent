# KSR888 GameXaGlobal DB-Backed Catalog

Use this reference when changing KSR888 provider/game listing, images, or launch flow around GameXaGlobal.

## Core rule
- GameXaGlobal remains the upstream source of truth for provider/game metadata.
- Frontend rendering should prefer local DB/cache fields populated by sync, not live API calls on every request.
- Store and reuse image URLs from DB fields such as `provider_image`, `banner`, `mobile_banner`, and `game_image` so pages stay light.

## Preferred flow
1. Sync provider/game records and images from GameXaGlobal into the local DB.
2. Build front-facing objects from DB rows or cached transient mappings.
3. Use cache version bumps (`v2`, `v3`, etc.) when switching source shape or filtering logic.
4. Keep fallback asset images for missing provider artwork.
5. Route play buttons to the existing launch path, but allow remote GameXaGlobal lookup if a game code is not found locally.

## Querying guidance
- Prefer queries that explicitly prioritize `providerapi = gamexaglobal` and `game_api = gamexaglobal` when the column exists.
- Avoid relying only on `provider_status = 1` for visibility; legacy rows may have null or mixed status values.
- For front lists, normalize remote API payloads into model-like transient objects, then cache the result.

## Verification used in this repo
- Use `docker exec` into the app/db containers when PHP is unavailable on the host.
- Use MariaDB queries to count records and confirm image columns are populated.
- Use `curl` + `jq` against the live GameXaGlobal endpoints to confirm provider/game totals.
- If the host lacks `php`, do not block on local lint; validate in-container or by inspecting runtime behavior instead.

## Common pitfalls
- Fetching provider/game images directly from the API during render makes the site heavy.
- Forgetting to bump cache keys can leave old provider/game data visible.
- Hardcoding legacy provider names in admin or front views reintroduces stale branding.
- Using status-only filters can hide valid GameXaGlobal rows that are intentionally stored inactive or legacy.
