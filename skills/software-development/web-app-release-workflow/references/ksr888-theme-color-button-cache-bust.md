# KSR888 theme color/button cache-bust

Use this when a live PHP-hosted KSR888 theme change is visible in source but not yet obvious on the public site.

## What worked
- Rename or version the stylesheet path in the PHP entry page, e.g. `dekstop.luxury.css?v=...` and `mobile.luxury.css?v=...`.
- Verify the rendered HTML points to the new stylesheet URL before changing more code.
- Fetch the stylesheet URL directly with a cache-busting query string and confirm the new markers exist in the live response.
- For button-only changes, add a late override that targets common CTA classes plus generic `button`, `a.btn`, `input[type=submit]`, etc., then set the new visual baseline in one place.
- If a global visual filter desaturates banners, add a banner-specific override that restores `filter: none`, `mix-blend-mode: normal`, and `opacity: 1` for `.banner img`, `.banner-carousel img`, `.banner-carousel .item img`, and `.banner-carousel .carousel-inner img`.

## Pitfalls
- A successful container rebuild does not prove the browser has picked up the new CSS.
- Renaming only the CSS file is not enough if the PHP entry page still points to the old path.
- Global color/filter overrides can accidentally wash out banner artwork.

## Verification
- `curl`/HTTP fetch the live HTML and stylesheet.
- Check the stylesheet version token in the rendered HTML.
- Rebuild and recreate the web container with the live DB env.
- If the browser still shows stale styles, hard-refresh or use a renamed stylesheet path.
