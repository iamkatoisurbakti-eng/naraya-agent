# KSR888 mobile deposit UX

Session note: the deposit page at `resources/views/account/deposit.blade.php` needed mobile-specific work because the form was visually present but not ergonomic on small screens.

## What worked
- Keep the main form submit as a normal POST to `route('create-payment')`.
- Add `@section('content')` so the Blade content is actually rendered by the layout.
- On mobile, reduce padding and card radius, and switch quick amounts to 2 columns.
- Add a small mobile-only instruction panel near the top of the form.
- Add a sticky bottom CTA labeled `Deposit Cepat` that is only visible on mobile.
- Sticky CTA should:
  - scroll/focus the nominal field if empty
  - call `requestSubmit()` when a valid nominal is already filled
  - fall back to `form.submit()` when `requestSubmit()` is unavailable
- Keep the sticky CTA above the bottom nav/footer so it does not overlap the page controls.

## Pitfalls
- A mobile deposit form can appear “broken” even when the backend is fine if the Blade section is not yielded by the layout.
- Heavy AJAX/QR rendering logic can hide the simplest successful path; prefer a direct submit path first.
- `required` file uploads in alternate QRIS/manual flows can block deposit UX on mobile.
- If the page already has a fixed bottom footer, reserve extra bottom margin on the form card and position the sticky CTA above it.

## Verification
- Clear compiled views and application cache after editing the Blade.
- Restart the web container.
- Re-open `/account/deposit` on a real mobile viewport and confirm:
  - the form renders
  - the sticky CTA appears
  - the CTA scrolls/focuses the nominal field when empty
  - the CTA submits when nominal is filled
