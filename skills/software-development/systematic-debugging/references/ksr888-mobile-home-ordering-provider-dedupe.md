# KSR888 mobile home ordering + provider dedupe

Use this when a KSR888 mobile homepage section is in the wrong order or a provider/game strip shows duplicates.

## Proven pattern
- Mobile layout lives in `resources/views/layouts/main/main.blade.php`.
- Homepage content lives in `resources/views/welcome.blade.php` under `@elsedesktop`.
- If a section must appear under the progressive jackpot, remove it from the mobile layout include chain and place it directly after the jackpot block in `welcome.blade.php`.
- For live imported PHP containers, host edits are not enough: copy the edited file into `nusantara-ai-saas-ksr888-web-1` and restart the container before verifying.

## Provider GameXaGlobal dedupe rules
- Source provider list from `SgProvider` where `provider_status = 1`.
- Deduplicate by normalized `provider_code`.
- Keep only providers with at least one usable image:
  - `frontend_mobile_image`
  - `frontend_provider_image`
  - `frontend_banner_image`
- If duplicate provider codes exist in the DB, keep the first provider record that has a valid image.

## GAME TERPOPULAR rules
- Show one game per active provider.
- Build the list from active provider codes, group `SgGame` rows by `game_provider`, then pick the first game per provider.
- Drop any game with an empty `game_image` before rendering.
- If the result is cached, bump the cache key after changing the selection logic.

## Verification
- Use a mobile User-Agent curl against `https://ksr888.online/`.
- Confirm HTML order by searching for `jackpot_amount`, `homeBannerCarousel`, `Provider GameXaGlobal`, and `GAME TERPOPULAR`.
- Use `tinker` or direct DB queries inside the live container to count unique provider codes and confirm the rendered provider/game counts.