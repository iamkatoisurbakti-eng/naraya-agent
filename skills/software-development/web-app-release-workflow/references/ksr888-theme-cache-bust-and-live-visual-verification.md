# KSR888 theme cache-bust and live visual verification

Use this when a PHP-hosted site updates a theme CSS file but the live page still looks unchanged.

## What happened
- Desktop/mobile theme CSS was updated successfully.
- The live HTML still referenced the unversioned CSS, so browser/edge cache could keep serving stale styles.
- Adding a cache-busting query string to the theme stylesheet links in the PHP entrypoints forced the browser to fetch the new CSS.

## Reliable verification pattern
1. Fetch the live HTML with a browser-like UA and confirm the stylesheet href includes the new version token.
2. Fetch the stylesheet URL directly with the same token and grep for the new markers.
3. Rebuild and recreate the PHP web container with the live DB env.
4. If the browser still appears unchanged, hard-refresh or test in incognito before changing more CSS.

## Practical notes
- For KSR888, the source entrypoints are:
  - `KSR888/site/dekstop/index.php`
  - `KSR888/site/mobile/index.php`
- The theme files were cache-busted by changing the href to versioned URLs like `Content/Theme/dekstop.css?v=...` and `Content/Theme/mobile.css?v=...`.
- Direct HTML checks matter more than build success for visible theme changes on cached PHP pages.
