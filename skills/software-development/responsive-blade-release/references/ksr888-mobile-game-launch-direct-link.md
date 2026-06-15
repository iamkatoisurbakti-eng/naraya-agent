# KSR888 Mobile Game Launch Direct-Link Fix

Date: 2026-05-13

Problem
- Mobile users could tap a game card but launch did not reliably open the game.
- Some mobile markup still used `target="_blank"` / `rel="opener"` and login-gated classes on launchable cards.

Fix pattern used
- For authenticated mobile cards, use a direct same-tab `href` to `/game_process/{game_code}/{game_provider}`.
- Keep `onclick="window.location.href='...' ; return false;"` only as a fallback enhancer, not as the sole launch path.
- Remove `target="_blank"` and `rel="opener"` from mobile game cards.
- Keep `login-alert` only on guest cards that should route to `/masuk`.
- Add tap-friendly CSS on the card: `display:block`, `cursor:pointer`, `touch-action: manipulation`, `-webkit-tap-highlight-color: transparent`.

Verification
- Recheck the live mobile HTML with an iPhone UA and confirm playable cards point to `/game_process/...`.
- Confirm guest cards still point to `/masuk`.
- Restart the live `ksr888-web` container after copying the Blade view.
- If the page is still stale, verify the live container file, not just the repo file.
- If the card click works but launch returns to `/slots`, debug the controller/API path; common signatures seen in this session were `The account has been frozen. Please contact the administrator` (`10016`), `Player not found`, and generic `Failed to launch game` responses from the upstream launch API.
- In KSR888, verify the live mobile flow from the `ksr888-web` container, not only the repo file, because Blade/PHP changes may need a rebuild/restart before the mobile tap path and launch route reflect in production.