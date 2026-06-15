# Checkout address section polish

Use this note when the user wants a checkout page to match a screenshot more closely, especially the shipping-address block.

## Pattern used in this repo
- Keep the address block visually compact and card-like:
  - dark panel background
  - thin light border
  - modest radius
  - tighter vertical spacing than the rest of the page
- Keep field sizing consistent with a mobile-first checkout:
  - `44px` field height
  - `3px` radius for inputs when matching the reference tightly
  - short helper/status text below the address fields
- If the design calls for a Material-style heading look, use `Roboto` for the page typography, with `DM Sans` only as fallback.
- If the address apply button is intentionally removed, do **not** reintroduce it just because the old flow had one; keep the flow driven by the checkout button and address validity.
- When address becomes valid/applied, auto-scroll to the `Checkout` CTA and focus it if possible.
- Keep `scrollIntoView()` and `focus()` behind feature checks so browser-less test runs do not crash.

## Verification
- Confirm the live HTML contains the compact address card styling and the `Roboto` font import.
- Smoke-test that entering `addr1` enables checkout and that the page scrolls/focuses the `Checkout` button after the address is applied.
- If the UI still has legacy `apply` handlers in JS, remove the dead DOM wiring so only the status helper remains.
