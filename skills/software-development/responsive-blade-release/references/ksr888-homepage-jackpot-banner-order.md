# KSR888 homepage jackpot/banner order

Use this reference when a KSR888 homepage request is about moving the banner slider, ticker, or other promo block relative to the progressive jackpot section.

## Pattern
- The homepage `welcome.blade.php` may render the jackpot block separately from `content.home_banner_slider`.
- To place the slider under the progressive jackpot, render `@include('content.home_banner_slider')` immediately after the jackpot container and before the main `app-wrapper` content.
- Keep the banner markup in the partial; only move the include position in the parent view.

## Live verification
- Verify rendered HTML order, not just file edits.
- Check that `progressive-jackpot-small.gif` (or the jackpot marker) appears before `homeBannerCarousel` in the live HTML.
- If a ticker is also present, confirm it still renders in the intended spot under the jackpot and above the main content.
- For header-order changes, confirm `LOGIN`/`DAFTAR` appear before the announcement strip in the rendered desktop header.

## Header/top-bar order
- For requests like "buat login daftar di paling atas", edit `resources/views/layouts/main/master.blade.php` instead of the homepage view or `content/navdesktop.blade.php`.
- Put auth buttons at the start of the desktop top row (`.flex-row.top.text-right`) before the announcement, complain button, social icons, and language controls.
- On KSR888, the host repo may not be live-mounted into the running container, so copy the Blade file into `nusantara-ai-saas-ksr888-web-1` and restart before verifying.

## Pitfalls
- Editing the host file alone is not enough on KSR888; copy the updated Blade file into the live container and restart/recreate the web container if the app is not bind-mounted.
- If the include is moved but the live page does not change, inspect the rendered HTML for stale output before assuming the view logic is wrong.
- Reordering sections can accidentally duplicate or hide the banner if the include remains in an old location elsewhere in the template.
