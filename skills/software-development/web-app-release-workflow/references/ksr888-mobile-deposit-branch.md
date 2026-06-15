# KSR888 mobile deposit branch fix

Use this reference when KSR888 reports the deposit page shows on desktop but is blank or missing on mobile.

## Root cause pattern
- The Blade view used `@desktop` for the desktop implementation and the mobile branch was absent or incomplete.
- In this repo, the desktop branch can render correctly while the mobile user-agent sees nothing if `@elsedesktop`/mobile markup is missing or not wrapped in `@section('content')`.

## Fix pattern
1. Keep the desktop deposit form intact.
2. Add a full mobile branch under `@elsedesktop` with its own `@section('content')`.
3. Put the actual deposit form in the mobile branch, not just helper text or a CTA button.
4. Use a simple, self-contained mobile layout:
   - heading + short subtext
   - nominal input
   - quick amount buttons
   - normal submit button to `route('create-payment')`
5. Avoid depending on a sticky CTA to make the form visible; the form itself must render on mobile.
6. If a sticky CTA is added for UX, make it optional and remove it when the user asks for it.

## Verification
- Test with a mobile user-agent, not only desktop.
- Clear compiled views and app cache after deploying the Blade change.
- Confirm the live HTML includes the mobile branch markers and the deposit form fields.
