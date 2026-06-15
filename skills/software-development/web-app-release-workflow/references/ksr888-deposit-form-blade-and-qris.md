# KSR888 deposit form and QRIS submit fixes

Use this reference when the KSR888 deposit page or QRIS/manual deposit flow stops rendering or submits silently.

## Symptoms observed
- `/account/deposit` redirected or rendered without the deposit section.
- The deposit button appeared dead because the form relied on client-side AJAX and failed without visible feedback.
- Manual/QRIS modal submission could be blocked by a required file upload even when no receipt was attached.

## Root causes found
- Blade structure issue: the deposit view needed a real `@section('content')` wrapper so the main layout would render it.
- AJAX submit hid failures; switching to a normal form submit made server-side errors visible.
- A `required` attribute on the QRIS/manual receipt upload prevented submission when users did not attach a file.

## Fix pattern
1. Ensure the deposit Blade view is wrapped in the section expected by the base layout.
2. Prefer a normal POST submit for the deposit action unless there is a proven reason to use AJAX.
3. Remove `required` from optional receipt/file inputs in QRIS/manual modals.
4. After patching, clear view/cache and restart the live web container before verifying again.

## Verification
- Open `/account/deposit` and confirm the section renders in the live app.
- Submit the form without a receipt file if the flow allows it.
- Check browser/network or server logs for redirects, validation failures, or cache path errors.

## Pitfalls
- A page can look “fixed” in source while live still serves stale compiled views; always clear view cache.
- If the page still does not appear, inspect the layout for a missing `@section('content')` / `@yield('content')` pair before chasing controller logic.
- Optional inputs should not be marked required just because a related modal supports file uploads.
