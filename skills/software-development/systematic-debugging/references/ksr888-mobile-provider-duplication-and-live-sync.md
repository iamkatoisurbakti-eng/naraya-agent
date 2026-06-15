# KSR888 mobile provider duplication and live sync

Session notes:
- The mobile homepage showed the same "GAME TERPOPULAR" block twice because `welcome.blade.php` included `content.gameNew` in the home shell while the mobile branch in `layouts/desktop/gamerow.blade.php` also rendered the same section.
- Fix was to keep the section in one place only and let the shared partial handle the breakpoint-specific rendering.
- For this repo, host edits are not always reflected in the running KSR888 web container. After changing PHP/Blade files, copy them into `nusantara-ai-saas-ksr888-web-1` and restart the container before validating.

Verification pattern:
- Check rendered HTML for desktop and mobile user agents separately.
- Count the section title / unique IDs in the response body.
- Confirm only one instance appears per page, not just visually in the browser.
