# KSR888 mobile provider-image cleanup

Use this when the KSR888 mobile front still shows legacy KSR888 artwork or provider rows need to resolve images from GameXaGlobal/provider API data.

## Session pattern
- Mobile/home UI should prefer provider API images over any legacy local KSR888 asset.
- For game cards, the safest fallback order is:
  1. `frontend_mobile_image`
  2. `frontend_provider_image`
  3. `frontend_banner_image`
  4. peer game image from the same provider
  5. first non-KSR888 image in the global `games` table
  6. legacy local icon only as the last fallback
- If a provider is missing image data in the DB, backfill from the provider API before touching Blade templates.

## Practical fix used
- Added a slider-only home view for the supplied banner files and mounted it into the home layout.
- Patched the `SgGame` image accessor so legacy `ksr888` URLs are replaced by provider/game API images.
- Cleaned the DB with a provider/game image sync so the front no longer depends on stale KSR888 URLs.

## Live verification
- Check rendered pages with `curl` and search for legacy image strings:
  - `ksr888.online/assets/img/logo.png`
  - `ksr888-icon-20260509c.png`
  - `ksr888-logo-20260509c.png`
- Verify the homepage contains the banner slider marker and the expected section title.
- Re-run focused tests after image-resolution changes, especially provider sync and API-only settings tests.

## Deployment notes
- In this repo, source edits may not be live inside `ksr888-web` until the container is rebuilt/recreated or the changed files are copied into the container.
- For view-only hotfixes, `docker compose cp` is a valid fast path before restarting the container.
