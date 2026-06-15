# KSR888 provider/game section redirects to `/slots`

Use this reference when KSR888 front sections must make provider/game tiles or titles open the provider game slot landing page.

## What changed in this session
- Mobile `content/provider.blade.php` title `Provider Game` was made clickable and routed to `{{ url('/slots') }}`.
- Mobile `content/gameNew.blade.php` title `GAME TERPOPULAR` was made clickable and routed to `{{ url('/slots') }}`.
- Mobile popular cards were also routed to `{{ url('/slots') }}` so the whole card area behaves consistently.
- Desktop `layouts/desktop/providerrow.blade.php` and `layouts/desktop/gamerow.blade.php` titles were also linked to `/slots` for parity.

## Verification pattern
1. Deploy the edited Blade files into the live `nusantara-ai-saas-ksr888-web-1` container.
2. Restart the container so Blade caches and PHP render the new markup.
3. Verify via a tiny PHP script or `curl` that rendered HTML contains `/slots` on:
   - provider title
   - GAME TERPOPULAR title
   - popular card hrefs
4. Prefer checking both mobile and desktop user agents if the page has responsive branches.

## Pitfalls
- If only the title is linked but cards still point at detail pages, the UX feels inconsistent; update both when the design intent is "everything opens provider slot page."
- Keep the redirect target as `url('/slots')` unless the product explicitly defines a different landing route.
- Do not hardcode hostnames in Blade; use Laravel URL helpers so the same template works across environments.