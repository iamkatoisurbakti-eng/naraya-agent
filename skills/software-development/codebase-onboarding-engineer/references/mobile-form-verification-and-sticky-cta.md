# Mobile form verification and sticky CTA

A reusable release pattern for Laravel/Blade mobile forms with fixed bottom navigation.

## Use when
- A form is visible on desktop but hard to use on mobile.
- A fixed bottom nav/footer overlaps the primary action.
- The simplest submit path works better than AJAX or in-place rendering.

## Pattern
1. Make sure the Blade section is actually yielded by the active layout.
2. Keep the main submit as a plain form POST when possible.
3. Add a compact mobile-only instruction panel near the top of the form.
4. Add a sticky bottom CTA only on small screens.
5. Sticky CTA behavior:
   - if required input is empty, scroll/focus the field
   - if input is filled, call `requestSubmit()`
   - fall back to `form.submit()` if needed
6. Add extra bottom spacing to the main card so the sticky CTA does not cover content.

## Verification
- Clear view cache and app cache.
- Restart the web container.
- Check the page in an actual mobile viewport, not just desktop responsive mode.
- Confirm the sticky CTA is above the fixed footer and does not hide the last form controls.
