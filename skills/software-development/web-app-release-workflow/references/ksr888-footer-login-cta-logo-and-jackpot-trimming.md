# KSR888 footer/login CTA, logo scaling, and jackpot trimming

Use this note when polishing KSR888 mobile/desktop chrome after the luxury theme is already in place.

## What changed successfully in this session
- Mobile footer anchors were styled as strong pill buttons with clear active state.
- Desktop login/register/live-chat/logout CTA buttons were styled as premium buttons with consistent padding, radius, shadow, and uppercase treatment.
- Mobile logo was enlarged safely by targeting `.site-header .logo img` with responsive `max-width` / `max-height` instead of changing the image asset.
- The `Jackpot Play` block was removed by deleting the jackpot section from:
  - `KSR888/site/mobile/template/home.php`
  - `KSR888/site/dekstop/template/home.php`
- After removal, desktop/mobile HTML was verified with live HTTP checks to confirm `Jackpot Play`, `jackpot-play-logo`, and `progressive-jackpot` were gone.

## Practical pattern
1. If the header logo looks too small on mobile, prefer CSS sizing in the luxury theme:
   - `.site-header .logo img`
   - keep `width: auto`
   - cap `max-width` and `max-height`
   - preserve `object-fit: contain`
2. If the bottom nav feels flat, style the actual anchor elements rather than wrapping containers:
   - padding
   - border radius
   - shadow
   - stronger active state
3. If the user wants a visible promo/jackpot element removed, search for the visible label first, then remove the whole markup block from the page template.
4. Rebuild the PHP image, recreate the container with the live DB env, and verify the public host directly with cache-busted HTTP checks.

## Verification strings
- `Jackpot Play`
- `jackpot-play-logo`
- `progressive-jackpot`
- `fixed-footer a[data-active="true"]`
- `site-header .logo img`
