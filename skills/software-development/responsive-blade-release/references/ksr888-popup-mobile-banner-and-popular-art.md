# KSR888 popup/mobile banner and popular-art workflow

Session-derived notes for responsive Blade work on KSR888.

## Popup banner mobile fix pattern
- Source file can live on the host, but the live web container must receive the file under the public storage path before the homepage can render it.
- If `genral_settings.popup` is `0`, the frontend will try to render `/storage/0` unless the view falls back.
- Safer flow:
  1. Copy the image/video into `storage/app/public/post-images/`.
  2. Copy the same file into `public/storage/post-images/` when the environment does not have a Laravel storage symlink.
  3. Update the active `genral_settings` row so `popup` points to `post-images/<filename>`.
  4. Keep `statusPopup = 0` for active display.
  5. Verify the mobile UA HTML contains the filename and the asset returns HTTP 200.

## Mobile GAME TERPOPULAR art
- For the mobile popular-games strip, the most reliable approach is to use local art copied into `public/assets/img/game-populer/`.
- Normalize filenames to simple stable names like `game-populer-01.webp` rather than spaces or parentheses.
- Verify the HTML with a mobile user-agent and confirm the asset URLs return HTTP 200.

## Verification checks
- Mobile HTML contains the popup filename or popular-art filename.
- Desktop/mobile branches both still render the page.
- Live asset URL returns 200.
- No `/storage/0` references remain in the rendered homepage.
