# KSR888 GAME TERPOPULAR mobile duplication notes

Use this when the home page or mobile layout shows duplicated popular-game cards, repeated blocks, or inconsistent click behavior.

## What happened in this session
- The homepage had the popular-games section rendered in more than one place.
- Mobile and desktop used different branches, but the same section could still appear twice if included from both the home page and the shared layout.
- The visible duplication was reduced by removing the extra include from `welcome.blade.php` and keeping one authoritative include path.
- The popular-game list also needed deduplication by normalized game name, because the top-N source data contained repeated names with different providers/codes.

## Checks to run
1. Search for all includes or renders of the popular-games partial.
2. Confirm whether the page is using shared layout + page-specific include simultaneously.
3. Inspect the data source before the view:
   - dedupe by normalized `game_name`
   - fall back to `game_code` if needed
4. Verify mobile and desktop branches separately:
   - mobile should render one carousel/list
   - desktop should render one grid/list
5. Reload the live page and confirm only one visible `GAME TERPOPULAR` block per device.

## KSR888-specific pitfall
- Host source edits may not affect the live web container immediately.
- If the container is not bind-mounted, copy the updated file into `nusantara-ai-saas-ksr888-web-1` and restart the container before verifying.

## Verification
- Use a mobile user-agent and a desktop user-agent against `https://ksr888.online/`.
- Count the `GAME TERPOPULAR` block once per device.
- Confirm the first few cards are unique and that clicking a provider/game goes to the expected detail or launch route.
