# KSR888 GameXaGlobal full game image sync

Context: KSR888 (`/root/nusantara-ai-saas/KSR888/site`) needed all game/provider images pulled from the GameXaGlobal API into the local `providers` and `games` tables.

## Useful workflow
1. Inspect existing integration first:
   - `app/Http/Api/gamexaglobal.php`
   - `app/Http/Controllers/GameController.php` (`syncGameXaGlobal`, image helpers, provider/game payload parsing)
   - `app/Models/SgProvider.php` and `app/Models/SgGame.php` for proxying image URLs.
2. Fetch providers with `gamexaglobal->providers()` and build a provider map keyed by both `CODE:TYPE` and `CODE`.
3. Fetch all games from `/api/games?page=N&limit=1000`, then also fetch every provider-specific endpoint `/api/games/provider/{providerCode}`. Provider-specific endpoints can fill images/details that the broad games endpoint misses.
4. Normalize image fields broadly. Useful keys observed/handled:
   - games: `game_image`, `image`, `image_url`, `thumbnail`, `thumbnail_url`, `logo`, `logo_url`, `icon`, `icon_url`, `banner`, `banner_url`, `cover`, `cover_url`, `picture`, `picture_url`, `img`, `img_url`
   - providers: `provider_image`, `image`, `image_url`, `logo`, `logo_url`, `icon`, `icon_url`, `thumbnail`, `thumbnail_url`, `banner`, `mobile_banner`
5. If a game has no direct image from the API, fallback to provider image/banner/mobile_banner rather than leaving `game_image` empty.
6. Upsert games by `(game_code, game_provider)` and providers by `(provider_code, provider_type)`. Mark `game_api = 'gamexaglobal'` when the column exists.
7. Clear catalogue caches after DB writes:
   - `game-library:providers`
   - `game-library:account`
   - `ksr888:home-catalog`
   - `ksr888:gamexaglobal:providers`
8. Verify DB coverage: count total games, missing `game_image`, and sample live `/game-image-proxy?...` requests.

## Runtime/tooling pitfalls
- Running Laravel bootstrap scripts inside the PHP container with `docker compose exec -T ... php ...` can throw Symfony `StreamOutput class needs a stream`. Use a real PTY: `docker compose exec ksr888-web php tmp/sync_all_game_images.php` with the terminal tool `pty=true`.
- If a script is created on the host after the container was built, either rebuild/recreate the container or copy it in with `docker cp ... nusantara-ai-saas-ksr888-web-1:/var/www/html/tmp/...` before running.
- Avoid printing provider tokens or env values; only report counts and status.

## Session result example
- Providers from API: 68
- Provider images saved: 68
- Games synced: 6,656
- Game images saved from API/provider: 6,656
- Inserted: 0, updated: 6,656
- API missing images: 0
- DB total games: 11,467
- DB games with images: 11,467
- DB missing images: 0
- Provider endpoint errors: 0
- Duration: ~75 seconds
