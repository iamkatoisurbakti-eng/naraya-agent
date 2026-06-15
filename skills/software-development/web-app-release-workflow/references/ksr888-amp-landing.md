# KSR888 AMP landing page notes

Use this when turning the imported KSR888 PHP host into an AMP landing page.

## Pattern
- Keep the source of truth in `KSR888/site/rtp.php`.
- Keep AMP media local to the host; copy the reference images into `KSR888/site/assets/img/` and point `<amp-img>` at those files.
- Favor a compact mobile-first layout: logo/header, hero banner, jackpot strip, provider image, then CTA buttons.
- Do not force the page into the Node/Vite app; this host is PHP and should stay in the PHP stack.

## Verification
- Run `docker compose exec -T ksr888-web php -l /var/www/html/rtp.php`.
- Rebuild the `ksr888-web` container and confirm `docker compose ps` shows it healthy/up.
- Grep the rendered PHP/HTML for the expected AMP sections and asset URLs.
- If browser automation fails with Chromium singleton/profile errors, fall back to container-side HTML/asset verification.

## Pitfalls
- Remote CDN assets can time out or be blocked; prefer local images for banner/provider sections.
- AMP pages need valid `amp-img` dimensions and a canonical URL.
- Keep the design readable on mobile; the page should still work even if the browser smoke path is unavailable.
