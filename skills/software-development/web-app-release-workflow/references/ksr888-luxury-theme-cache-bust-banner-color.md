# KSR888 luxury theme cache-bust and banner color preservation

Use this when PHP-hosted KSR888 theme changes appear live in build/deploy output but not in the browser.

## What worked
- The page HTML was updated to point at a new stylesheet filename plus versioned query string, e.g. `Content/Theme/dekstop.luxury.css?v=...` and `Content/Theme/mobile.luxury.css?v=...`.
- The exact live CSS file was verified directly with HTTP, not just the homepage HTML.
- A separate stylesheet copy was safer than repeatedly editing the same cached filename when the edge/browser kept serving stale bytes.

## Important pitfall
- A global media filter used for the black/gold luxury look can make banners look desaturated or grayscale.
- If banners lose color, add a late CSS override that targets banner-specific selectors only, for example:
  - `.banner img`
  - `.banner-carousel img`
  - `.banner-carousel .item img`
  - `.banner-carousel .carousel-inner img`
- Keep those banner selectors on `filter: none !important;`, `mix-blend-mode: normal !important;`, and `opacity: 1 !important;` so decorative media stays colorful while the rest of the site can stay stylized.

## Verification
1. Fetch the live HTML and confirm it references the new stylesheet version string.
2. Fetch the live stylesheet URL directly and grep for the new theme markers.
3. If an image style change looks wrong, check whether a broader `img` rule is overriding the image-specific selectors.
4. Rebuild and recreate the PHP web container after the source update, then recheck the live host.
