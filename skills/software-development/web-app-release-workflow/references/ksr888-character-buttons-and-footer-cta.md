# KSR888 character buttons and footer CTA

Use this pattern when polishing the KSR888 PHP host’s navigation/CTA chrome.

## What changed in this session
- Desktop top-menu items (`Hot Games`, `Slots`, `Live Casino`, `Togel`, `E-Games`) were restyled as animated pill buttons.
- Mobile main-menu entries were given the same character treatment with sheen/bob motion, clearer spacing, and strong contrast.
- Mobile fixed-footer anchors and desktop login/register/live-chat/logout CTAs were aligned to the same black/white luxury button language.
- Decorative `Jackpot Play`/progressive-jackpot branding was removed from the homepage so the menu/buttons carry the visual weight instead.

## Useful selectors
- Desktop: `.top-menu > li > a`, `.top-menu .game-list li a`
- Mobile: `.main-menu-outer-container main > a`, `summary`, and nested menu links
- Footer/login: `.fixed-footer a`, `.login-panel .login-button`, `.login-panel .register-button`, `.topbar-left-section .topbar-item a.live-chat`, `.btn-logout`

## Implementation notes
- Use late CSS overrides in `dekstop.luxury.css` and `mobile.luxury.css`.
- Add motion sparingly: one bob animation plus one sheen overlay is enough for character.
- Keep icons grayscale/contrast-heavy so the black/white theme stays readable.
- Cache-bust the CSS in both PHP entry pages after the patch.
- Verify by fetching live HTML/CSS directly and checking the intended labels/tokens still render after deploy.
