# KSR888 black/white theme and banner pruning

Use this when the user wants the KSR888 PHP host to be visually restyled and specific banner slides removed.

## Theme pass
- Update the source-of-truth theme files only:
  - `KSR888/site/dekstop/Content/Theme/dekstop.css`
  - `KSR888/site/mobile/Content/Theme/mobile.css`
- Add overrides at the end of the theme file so the legacy PHP styles remain intact but are superseded.
- For a full dark treatment, force:
  - `html, body` background to black
  - main containers/panels/cards/modals to black or near-black
  - text to white
  - important borders/dividers to light gray/white
- For animated CTAs/buttons, prefer a small set of reusable selectors covering:
  - `button`, `.btn`, `a.btn`
  - submit/reset inputs
  - feature-specific CTAs like login, claim, download, info, and modal action buttons
- Use subtle motion only:
  - shimmer/background-position animation
  - small hover lift/scale
  - soft brightness pulse
- Keep the animation readable; avoid heavy flashing or broad hue cycling.

## Banner slide pruning
- In the slider templates, remove early slides by slicing the resolved banner array after the DB/fallback merge:
  - `array_slice($bannerItems, 2)` removes the first two items
- Apply the same pruning in both:
  - `KSR888/site/dekstop/template/slider.php`
  - `KSR888/site/mobile/template/slider.php`
- Keep the carousel markup unchanged so indicators and active state still work.

## Rebuild and verification
1. Rebuild the PHP image:
   - `docker compose build ksr888-web`
2. Recreate the web container with the live DB env from the DB container or production env file.
3. Verify the live CSS files directly with a cache-busting query string and confirm the new markers are present:
   - `ksr-btn-shimmer`
   - `color-scheme: dark`
4. Verify the public pages still return `200`.
5. If browser automation fails with Chromium singleton/profile errors, fall back to HTTP verification plus live CSS/bundle inspection rather than repeating the same browser launch.

## Pitfalls
- Do not change build artifacts instead of source CSS.
- Do not remove carousel markup unless the user explicitly asks to remove the slider entirely.
- If the container starts returning `500`, inspect the PHP web container env and DB auth before blaming the UI patch.
