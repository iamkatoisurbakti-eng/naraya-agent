# KSR888 GameXaGlobal launch and provider-resolution notes

Session goal: eliminate provider launch fallbacks to `/slots` and make GameXaGlobal provider/game launch resolve to the final URL.

Observed runtime facts
- Live GameXaGlobal provider catalog returned 68 providers.
- Live GameXaGlobal game catalog returned 6,656 games.
- KSR888 local DB was syncing GameXaGlobal provider/game rows and images into `SgProvider` / `SgGame`.
- Image sync should stay DB/cache-backed; avoid re-hitting provider image endpoints on every render.

Launch-debug findings
- After broadening provider launch candidate search, 47 providers launched successfully and 21 still fell back / failed.
- The remaining failures were not primarily a UI routing issue; the upstream API returned `Failed to launch game` / `Player not found`.
- For at least one failing provider (`MANCALA`), multiple launch payload variants still returned `Player not found`, including minimal payloads and variants with provider/type/username/user_code/lobby fields.
- This suggests the blocker is player provisioning/identity or provider-specific launch requirements, not just `game_uid` mapping.

Provider alias / resolution notes
- Some provider codes in DB do not match the API’s preferred alias directly.
- Confirmed remote aliases included: `2J`, `GALAXSYS`, `KM`, `MANCALA`, `PIX`, `SPRIBE`, `V8`, `YEEBET`.
- Reverse-alias matching is important for codes like `JILI_GAMING`, `GAME_ART`, `MANCALA`, `YEEBET`, `568WIN_SPORTS`, etc.
- Prefer trying both:
  1. local DB candidates filtered to `game_api=gamexaglobal`
  2. remote `provider/{code}` catalog
  3. global `games` catalog
  4. alias-expanded variants

Verification pattern that worked
- Use `docker exec <web-container> php ...` because host shell may not have PHP.
- Keep small deterministic debug scripts in `tmp/` for provider-by-provider checks.
- When a provider still falls back, inspect whether the API response says no player / player not found before changing frontend routing.

Practical implication
- If launch still fails after candidate expansion, treat the problem as upstream API compatibility or account/player setup, not as a front-end fallback bug.
- Continue debugging provider launch one provider at a time until the upstream API returns a final game URL instead of `/slots`.

Validated launch payload shape
- `buildGameXaGlobalLaunchPayload()` should emit:
  - `player_id`
  - `player_name`
  - `game_uid`
  - `provider_code`
  - `game_type` (normalized; fallback `SL`)
  - `lang: id`
  - `currency: IDR`
  - `lobby_url` from local resolver, e.g. `/slots/server-b/{provider}/{type}`
- A successful smoke check in the live container should use `docker compose exec -T ksr888-web php -r ...` with `require "vendor/autoload.php";` before reflecting controller methods.
- After editing source on the host, re-check the live container state because KSR888 PHP code is not bind-mounted into `ksr888-web`.