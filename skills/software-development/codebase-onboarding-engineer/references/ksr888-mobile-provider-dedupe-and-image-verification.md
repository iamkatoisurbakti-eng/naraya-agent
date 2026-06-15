# KSR888 mobile provider dedupe and image verification

Use this note when mobile slot/provider pages show duplicates or fallback to legacy KSR888 assets.

## What happened
- `SgGameController::categoryProviders()` can still emit alias duplicates from GameXaGlobal provider rows even after source filtering.
- In the live data, duplicate display pairs included aliases such as:
  - `Booongo` / `BNG`
  - `Play N Go` / `PLAYNGO`
- The final fix was applied in two layers:
  1. controller-side de-duplication of the provider collection
  2. blade-side `unique()` guard on the rendered list

## Recommended dedupe key
- Prefer normalized display name first, not provider code.
- Normalize by lowercasing and stripping non-alphanumerics.
- If the name is empty, fall back to provider code.
- Do not use image URL as the only key; it may hide valid alias rows that should collapse by name.

## Image verification rules
- Front mobile provider/game thumbnails must resolve from provider API / DB-synced fields.
- Provider image order used in the fix:
  - `frontend_provider_image`
  - `frontend_mobile_image`
  - `frontend_banner_image`
  - legacy KSR888 icon only as a last resort in views that still need a fallback
- Game image rule remains: if a stored `game_image` looks like a KSR888 asset, resolve to provider/peer/global non-KSR888 image instead.

## Verification commands
Run inside the web container:

```sh
php -l app/Http/Controllers/SgGameController.php
php artisan view:clear --no-ansi
php artisan cache:clear --no-ansi
curl -s -A "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.4 Mobile/15E148 Safari/604.1" http://127.0.0.1/slots
```

Then check:
- provider count vs unique provider name count
- zero `ksr888.online/assets/img` fallback hits in the rendered HTML
- duplicate names like `Booongo` and `Play N Go` are collapsed to one card each

## Operational pitfall
After editing PHP controllers/blade files on the host, make sure the live web container receives the updated files and is restarted if the app is not using a bind mount. A syntax-clean host file can still be stale in runtime until container sync/restart completes.
