---
name: responsive-blade-release
description: Release and verify responsive Laravel Blade pages, especially when desktop/mobile branches differ or one branch renders blank.
---

# Responsive Blade Release

Use this skill when shipping or debugging a Laravel Blade page that must render cleanly on both desktop and mobile, especially when the template uses custom branching such as `@desktop` / `@elsedesktop` or separate markup paths.

## When to use
- A page works on desktop but is blank, incomplete, or hidden on mobile.
- A Blade view has separate desktop/mobile branches.
- A sticky mobile CTA, helper text, or JS-only path is being considered as the main way to show important content.
- A deploy needs cache clearing and live verification on real user agents.

## Fix pattern
1. Identify the source-of-truth Blade view, not just the rendered HTML.
2. Verify both branches exist and are complete:
   - desktop branch
   - mobile branch
3. Make the mobile branch contain the real content, not only a button or note.
4. Keep the mobile layout self-contained:
   - clear title/subtitle
   - visible form fields
   - plain submit path
   - minimal JS that only enhances UX
5. If a sticky mobile CTA is added, treat it as optional UX only; remove it when it starts hiding or replacing the actual form.
6. For mobile game cards, prefer a direct same-tab `href` to the launch route on authenticated cards; do not rely on `target="_blank"` / `rel="opener"` for the primary launch path.
7. Keep `login-alert` only on guest-only cards that should route to `/masuk`; attaching it to playable cards can block the launch click.
8. If the HTML looks correct but launch still fails, verify the controller path with a live PHP probe in the container; mobile launch problems can actually be upstream API failures (for example frozen account, missing player, or provider not found) even when the tap/redirect path is fine.
9. For one-game mobile verification, test a single known game end-to-end on a mobile user-agent until you see the actual provider launch URL or the exact upstream rejection; do not stop at the click event.
10. If the provider returns `10016` / frozen-account-style errors after the card reaches `/game_process/...`, treat it as a provider/account issue, not a Blade/touch-target bug.
9. After editing the view, clear compiled views and app cache, then redeploy/restart the web container.
10. For ordering fixes, verify the rendered HTML sequence with a live user-agent or `curl` and confirm the intended element appears before its sibling in the response.

## Common pitfalls
- Desktop branch renders correctly, so the bug is missed unless a mobile user-agent is tested.
- `@desktop` / `@elsedesktop` logic leaves mobile with no `@section('content')` output.
- A sticky button or JS helper becomes the only visible control on mobile.
- The page looks fixed locally but old compiled views or app cache still serve stale markup.
- When the root homepage needs shared content on both desktop and mobile, consider placing the shared include in the master layout instead of duplicating it in `welcome.blade.php` branches.
- If a popup/banner is uploaded from an admin panel but never appears, check the controller storage path and the active settings row before assuming the Blade branch is wrong; a valid view with `popup = 0` will still render nothing.
- For KSR888 mobile provider/pop-up assets, normalize local files into `public/assets/...`, copy them into the live container, restart, then verify with a mobile user-agent curl plus direct asset HTTP 200s; see `references/ksr888-mobile-provider-file-assets.md`.
- Verification is done via desktop browser only; mobile rendering remains broken.
- For mobile GAME TERPOPULAR art, use local assets with stable filenames under `public/assets/img/...`; avoid relying on host-only files or names with spaces/parentheses if the live HTML or cache may normalize poorly.
- Verify with both desktop and mobile user-agents; a desktop-only check can miss the broken branch entirely.

## Verification checklist
- Test with a mobile user-agent or real phone viewport.
- Confirm the mobile HTML includes the actual form, not just helper text.
- For launch cards, confirm the rendered mobile HTML points to the launch route you expect and does not still expose a guest/login-only href on playable cards.
- Confirm submit works with JS disabled or minimal JS.
- Clear view and application cache after deploy.
- Reopen the live page and verify the mobile branch renders as expected.

## Reference
- For a concrete KSR888 example of a blank-mobile deposit page and the fix pattern, see `references/ksr888-mobile-deposit-branch.md`.
- For KSR888 homepage popup uploads that must be visible in frontend, see `references/ksr888-popup-admin-upload-public-storage.md`.
- For KSR888 homepage jackpot/banner ordering and live HTML-order verification, see `references/ksr888-homepage-jackpot-banner-order.md`.
- For KSR888 provider strips that should use active slot-game thumbnails, see `references/ksr888-provider-slot-preview-images.md`.
- For KSR888 provider strips that should use active slot-game thumbnails, see `references/ksr888-provider-slot-preview-images.md`.
- For KSR888 `GAME TERPOPULAR` slot-only 10-item selection and `game_code` dedupe, see `references/ksr888-game-terpopular-slot-top10.md`.
- For KSR888 popup/mobile banner assets and local popular-art deployment, see `references/ksr888-popup-mobile-banner-and-popular-art.md`.
- When mobile launch fails before the Blade branch renders, inspect the controller path first; object collections should be deduped by stable IDs like `game_code` instead of `Collection::diff()`. See `references/ksr888-game-launch-mobile-diff-pitfall.md`.
- If you need to restart or live-verify after copying PHP files into the KSR888 container, always confirm the mobile UA response returns 200 plus the expected game markup.
- For KSR888 game-launch regressions, verify both layers: the mobile card must point to `/game_process/...`, and the controller must return an external launch URL instead of redirecting back to `/slots`.

## KSR888 mobile provider/popup asset rules
- If a requested host file lives outside the web root, copy it into a stable public asset path before binding it into the Blade view.
- Prefer normalized filenames without spaces or parentheses for live assets; they are safer for cache-busted HTML, direct HTTP checks, and container copies.
- After changing a mobile asset or provider title, redeploy the view plus the public asset directory into the live container and verify with a mobile user-agent curl and direct asset HTTP 200s.
- If the desktop/mobile branches differ, verify both branches explicitly; a fix in the mobile partial does not imply the desktop shell changed.

## Homepage popular-games pitfall
- When mobile and desktop both need the same `GAME TERPOPULAR` content, keep the selection logic shared and cap it at 10 slot items.
- Deduplicate by `game_code`, not `game_name`; duplicate names can hide a valid game and reduce the rendered count.
- If the live count is off by one, verify the rendered HTML directly and check for stale home-catalog cache entries before changing the view again.
- For KSR888 provider slot-only carousel ordering, dedupe, and live verification, see `references/ksr888-provider-slot-carousel.md`.
- For KSR888 provider/game section links that should open `/slots`, see `references/ksr888-provider-game-slot-redirect.md`.
- For the mobile launch debug trail (direct-link fix + upstream failure signatures), see `references/ksr888-mobile-game-launch-direct-link.md`.
