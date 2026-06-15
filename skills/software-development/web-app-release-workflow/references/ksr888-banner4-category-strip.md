# KSR888 banner/4 category strip

Use this when the user wants KSR888 navigation/category buttons to resemble `KSR888/banner/4.png`.

## What the reference is
- `banner/4.png` is a horizontal PNG strip, about `1024 x 114`.
- It is best treated as a menu/navigation reference, not a logo or hero banner.
- The visual direction is dark base + pink/magenta strip accents + neon/glow character.

## Implementation pattern
- Apply the look in late CSS overrides so the legacy PHP/HTML structure stays intact.
- Desktop target areas:
  - `.top-menu`
  - `.top-menu > li > a`
  - `.top-menu .game-list`
- Mobile target areas:
  - `.main-menu-outer-container`
  - `.main-menu-outer-container main > a`
  - submenu/details elements that render the category strip
- Add small motion only: sheen, bob, glow pulse. Keep the menu readable and clickable.

## Cache-bust lesson
- When the visual change does not appear live, bump the stylesheet version string in the PHP entry page too.
- Verifying the CSS file alone is not enough; confirm the HTML actually points at the new `?v=` token.

## Verification
1. Rebuild/recreate the PHP web container.
2. Fetch the live HTML with a browser-like User-Agent.
3. Confirm the version token is present in the rendered HTML.
4. Fetch the live CSS URL directly and grep for the new marker class names.
5. If possible, do a real browser screenshot check on desktop and mobile.

## Practical markers from this session
- Desktop marker: `ksr-banner4-glow`
- Mobile marker: `ksr-mobile-banner4-glow`
- Live version token used: `20260509lux10`
- White-button rule remained in place: white background, black text
