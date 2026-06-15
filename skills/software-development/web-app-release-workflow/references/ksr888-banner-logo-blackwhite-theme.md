# KSR888 banner, logo, and black/white theme notes

Session learnings
- KSR888 banner assets live under `/root/nusantara-ai-saas/KSR888/banner/` and should be copied into `/var/www/html/banner/` by the PHP image so the live site serves them without depending on DB rows alone.
- The desktop and mobile sliders were updated to:
  - load rows from `tb_banner` as the primary source
  - fall back to files in `/banner/` when needed
  - use stable public URLs with `target="_blank"` and safe HTML escaping
- Banner images in this session were mixed aspect ratios (`1536x1024` and `1920x613`), so mobile needed a fixed crop strategy instead of free-height images.
- For mobile presentation, a practical fit was:
  - `aspect-ratio: 16 / 7`
  - `object-fit: cover`
  - small-radius clipping and a tighter indicator position
- The website logo was replaced by copying the chosen banner image to the web asset path used by the existing PHP templates and keeping the DB `tb_web.logo` value aligned with the public filename.
- A black/white full-animation theme was implemented by appending CSS overrides to the theme files rather than rewriting every component:
  - black page background
  - white text everywhere
  - grayscale/contrast filter on media
  - subtle animated background sheen using `body::before` / `body::after`
  - animated carousel indicators
  - button/panel overrides with `!important` where the legacy CSS was too specific

Pitfalls
- When the imported PHP app already uses a large theme stylesheet, the safest visual override is usually to append a compact override block near the end rather than editing many scattered selectors.
- If a live asset is on disk but not reflected on the site, verify the Docker image is copying the right directory and that the web container was recreated from the rebuilt image.
- If you swap the visible logo to a banner-style image, also ensure the favicon/icon path and backoffice/public asset mirrors are still valid.

Verification pattern
- Rebuild the PHP image.
- Recreate `ksr888-web` with the live DB env from the `ksr888-db` container.
- Verify:
  - `https://ksr888.online/dekstop/index.php` returns 200
  - `https://ksr888.online/mobile/index.php` returns 200
  - banner image URLs return 200
  - the CSS theme URLs contain the new override markers
- If browser automation fails with Chromium singleton/profile errors, fall back to HTTP fetch + bundle/CSS grep and direct asset checks.
