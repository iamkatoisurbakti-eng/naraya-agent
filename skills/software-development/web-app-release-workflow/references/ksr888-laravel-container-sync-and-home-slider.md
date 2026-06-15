# KSR888 Laravel container sync + home slider notes

When the KSR888 Laravel app is running inside Docker, the live web container may not see host-side edits until the changed files are copied into the container (or the image is rebuilt). In this session, the live service was `ksr888-web` and the app root inside the container was `/var/www/html`.

Useful verification pattern:
1. Copy edited source files into the running container.
2. Run `php -l` on the updated PHP/Blade files inside the container.
3. Run the focused PHPUnit tests.
4. Clear compiled views and caches.
5. Restart the web container.
6. Check the live homepage with curl and confirm the slider markup is present.

Home banner slider implementation notes:
- The homepage banner slider was built from five stored assets under `public/storage/post-images/`.
- The slide set used these files:
  - `ksr888-banner-naga-harimau-20260508194542.jpeg`
  - `ksr888-banner-link-merge-20260505161432.jpeg`
  - `ksr888-banner-magic-piggy-20260429134717.png`
  - `ksr888-banner-24d-spin-20260402155618.png`
  - `ksr888-banner-1872-20260505161432.jpeg`
- On the front mobile view, provider imagery should prefer provider images from GameXaGlobal (`frontend_mobile_image` -> `frontend_provider_image` -> `frontend_banner_image`) instead of KSR888 fallback art.
