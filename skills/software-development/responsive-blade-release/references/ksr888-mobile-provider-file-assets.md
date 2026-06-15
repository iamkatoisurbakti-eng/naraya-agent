# KSR888 Mobile Provider / Popup File Assets

This note captures the live-deploy pattern used for KSR888 when a mobile Blade section must render assets stored only on the host filesystem.

## Observed pattern
- Host-only files may live under `/root/nusantara-ai-saas/KSR888/site/...` or sibling folders like `/root/nusantara-ai-saas/KSR888/GAME POPULER` and `/root/nusantara-ai-saas/KSR888/site/FILEPR`.
- The web container reads from `/var/www/html/public/...`, so host files must be copied into a public asset path before the browser can fetch them.
- The mobile homepage/provider sections were verified by:
  1. copying host files into `public/assets/img/...`
  2. copying the updated Blade view into the live container
  3. restarting the web container
  4. checking mobile-user-agent HTML plus direct asset HTTP 200s

## Safe filename convention
- Prefer normalized names such as `filepr-01.png` or `game-populer-01.webp`.
- Avoid spaces and parentheses in live asset names when possible.
- If the source folder uses spaces/parentheses, rename files while copying into `public/assets/...`.

## Verification recipe
- Mobile HTML check:
  - `curl -sk -A 'Mozilla/5.0 (iPhone; ...)' https://ksr888.online/`
- Asset check:
  - `curl -sk -o /dev/null -w '%{http_code}' https://ksr888.online/assets/img/...`
- Confirm the rendered HTML contains the expected title or asset filename.

## Example asset mappings used on KSR888
- `/root/nusantara-ai-saas/KSR888/GAME POPULER/` -> `/public/assets/img/game-populer/`
- `/root/nusantara-ai-saas/KSR888/site/FILEPR/` -> `/public/assets/img/filepr-provider/`
- Popup banner file copied into `/storage/app/public/post-images/` and referenced via `Setting::popup`
