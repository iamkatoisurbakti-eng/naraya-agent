# PHP Theme Cache-Bust + Live Visual Verification

Use when a CSS/theme change in a PHP-hosted site is built and the live page still looks unchanged.

## Pattern
1. Confirm the rendered HTML really points to the new stylesheet URL.
   - Use a cache-busting query string on the CSS link in the PHP entry page.
   - Verify the live HTML contains the new query string, not just the source tree.
2. Fetch the exact live CSS URL directly.
   - Check for the new CSS markers in the response body.
   - Use the exact `?v=...` URL the browser will request.
3. Redeploy the web container after the source change.
4. Verify the public HTTPS page after deploy.
   - If possible, use a browser screenshot or DOM smoke.
   - If the browser tool is blocked by profile/socket errors, fall back to HTTP + live CSS grep.

## Pitfalls
- A successful build does not prove the browser received the new stylesheet.
- CSS-only theme edits on imported PHP apps are often masked by browser/CDN cache.
- Updating the stylesheet file without bumping the stylesheet URL in the entry page can make the live page appear unchanged.

## Good verification signals
- Live HTML contains the new stylesheet query string.
- Live CSS response contains the new markers.
- Public page returns 200 after redeploy.

## Session note
This repo’s KSR888 theme changes needed both the CSS override and an entry-page cache-buster bump before the visual difference was obvious live.