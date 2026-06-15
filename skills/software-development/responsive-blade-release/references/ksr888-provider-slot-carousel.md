# KSR888 provider slot carousel

Session note for the responsive Blade release workflow.

## Problem
KSR888 homepage section `Provider GameXaGlobal` needed to show slot-only providers on both mobile and desktop, with stable ordering and no duplicate provider cards.

## Working fix pattern
- Prepare the filtered collection in the controller, then pass it to the Blade view as `$slotProviders`.
- In the view, prefer `($slotProviders ?? $providers)` for the provider carousel.
- Filter to `provider_type = SL` for slot-only provider lists.
- Count game activity from slot games only (`game_type = SL` / `slot`) using a case/trim-insensitive filter.
- Dedupe by `provider_code` before render.
- Keep only providers with a valid frontend image.
- Score image priority as:
  1. `frontend_mobile_image`
  2. `frontend_provider_image`
  3. `frontend_banner_image`
- Bump the homepage cache key after changing provider selection logic.

## Verification
- Check live HTML on both mobile and desktop user agents.
- Confirm all rendered provider cards are unique and slot-only.
- If `artisan tinker` / shell quoting is flaky, use a standalone PHP verification script inside the live container instead.