# KSR888 provider/game section redirect to `/slots`

Use this reference when a responsive Blade homepage section should route both titles and cards to the provider slot landing page.

## What changed
- Mobile provider section title `Provider Game` was linked to `{{ url('/slots') }}`.
- Mobile `GAME TERPOPULAR` title was linked to `{{ url('/slots') }}`.
- Mobile popular cards were also linked to `{{ url('/slots') }}` so the whole card surface behaves consistently.
- Desktop provider and popular section titles were linked to `/slots` for parity where those partials are used.

## Verification pattern
1. Edit the Blade partials under the source tree.
2. Copy the changed view files into the live KSR888 container if the container is not bind-mounted to source.
3. Restart the web container so Blade output refreshes.
4. Verify rendered HTML with a small PHP script or curl + user-agent switch.
5. Check that the rendered output contains `/slots` in both the section title and card hrefs.

## Pitfalls
- Changing only the title leaves the cards still opening a detail page; patch both when the intent is “everything opens provider slot page.”
- Prefer `url('/slots')` over hardcoded absolute URLs so the same Blade works across environments.
- If the live site uses separate mobile/desktop partials, verify both user agents before considering the fix complete.