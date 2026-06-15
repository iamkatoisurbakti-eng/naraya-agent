# KSR888 mobile deposit branch fix

Use this reference when KSR888 reports the deposit page works on desktop but is blank or missing on mobile.

## Root cause pattern
- The Blade view used a desktop-only branch and the mobile branch was absent, incomplete, or not wrapped in the correct section.
- Desktop rendering can hide the issue unless the page is tested with a mobile user-agent.

## Fix pattern
1. Keep the desktop form intact.
2. Add a complete mobile branch with its own `@section('content')`.
3. Put the real deposit form in the mobile branch, not just helper text or a CTA button.
4. Keep the mobile layout self-contained:
   - title/subtitle
   - nominal input
   - quick amount buttons
   - normal submit path
5. Treat sticky CTAs as optional UX only; do not rely on them to make the form visible.

## Verification
- Test with a mobile user-agent or real phone viewport.
- Clear compiled views and app cache after deployment.
- Confirm the live HTML includes the mobile branch and the form fields.
