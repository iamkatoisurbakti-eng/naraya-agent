# Starlink root AMP static landing deploy

Session pattern from deploying `/root/amp_ksr888_branded.html` to `starlinkindonesia.shop`.

## Source/context
- App repo: `/root/nusantara-ai-saas`
- Supplied file: `/root/amp_ksr888_branded.html`
- Public source files created:
  - `web/public/amp_ksr888_branded.html`
  - `web/public/starlinkindonesia.html` (alias)
  - `web/public/ksr888-amp-logo.png`
- Runtime route added in `src/app.ts` Express fallback for host `starlinkindonesia.shop` and `www.starlinkindonesia.shop`.
- Caddy route added as explicit site block for `starlinkindonesia.shop, www.starlinkindonesia.shop` reverse-proxying to `app:3000`.

## Key gotchas
- The supplied HTML was only a fragment, not a full document. Wrap it with `<!doctype html>`, `<html>`, `<head>`, viewport, title, description, canonical, and a simple body layout.
- The logo path referenced `/mnt/user-data/uploads/...`, which is not production-served. Copy the real image into `web/public/` and update the HTML to `/ksr888-amp-logo.png`.
- Static file in `web/public` alone did not make the root domain serve it because the Express fallback has a generic landing handler for `/`. Add a host check before that generic root handler.
- `checkout.starlinkindonesia.shop` is separate and should continue serving `/KSR.html`; do not conflate it with the root `starlinkindonesia.shop` AMP page.
- Caddy’s `{$DOMAIN}` block does not cover this separate root domain, so add explicit HTTP redirect and HTTPS reverse-proxy blocks.
- Restarting Caddy can produce one transient `curl: (56) Recv failure`; retry after the restart.
- Browser automation on this host may fail with Chromium snap ProcessSingleton errors; use HTTP/curl marker verification.

## SEO/AMP expansion from follow-up
- If the user asks for Google index/traffic work on this domain, promote the fragment landing into a real AMP-valid document and verify with `npx --yes amphtml-validator`.
- Keep static source in `web/public/amp_ksr888_branded.html`; add support pages in `web/public/ksr888.html`, `web/public/situs-terpercaya.html`, and `web/public/situs-slot-gacor.html` when targeting those long-tail keywords.
- In `src/app.ts`, route `/`, `/ksr888`, `/situs-terpercaya`, and `/situs-slot-gacor` for host `starlinkindonesia.shop`; also serve a host-specific focused sitemap with only these URLs.
- Add valid `favicon.png`, `favicon.ico`, and `manifest.webmanifest` under `web/public/`; otherwise static fallback can return HTML for favicon/manifest requests.
- If performance is prioritized, use a text brand (`KSR888`) instead of the heavy PNG logo. Do not reintroduce `amp-img`, `<img>`, `og:image`, `twitter:image`, or manifest icon references after the user asks to remove the logo for performance.
- For AMP logo images with fixed-height layout, use `width="auto" height="54" layout="fixed-height"`. A duplicated `height` or numeric width fails AMP validation.
- For GSC API integration on this domain, see `seo-growth/references/google-search-console-oauth-and-starlink-loop.md`; service-account sharing can fail with “email tidak ditemukan,” so OAuth with `http://localhost:1/` redirect may be needed.
- See the SEO-side reference `seo-growth/references/starlink-amp-seo-24h-loop.md` for the scoring/debate/24h loop and responsible wording.
- If GSC automation is requested, store service-account JSON under `secrets/` with mode `600`, do not print private-key contents, and use a helper such as `scripts/gsc_starlink_check.py` to verify property permission before claiming GSC access. If the Search Console UI says the service-account email is “not found,” switch to OAuth Desktop credentials for the actual GSC owner account; do not keep retrying service-account user assignment.

- If the user removes a heavy logo/image for performance, do a full no-image cleanup: remove the visible `amp-img`/`img`, `og:image`, `twitter:image`, schema `logo`, and manifest icons; replace with lightweight text branding and update any running SEO/GSC loop prompt so future automation does not reintroduce the image.

## Verification commands
```bash
cd /root/nusantara-ai-saas
npm run build
bash scripts/deploy.sh
docker compose exec -T caddy caddy validate --config /etc/caddy/Caddyfile
docker compose restart caddy
curl -fsS -A 'Mozilla/5.0' 'https://starlinkindonesia.shop/?v=YYYYMMDD' \
  | grep -E 'KSR888|Situs Terpercaya|Situs Slot Gacor'
curl -fsS -A 'Mozilla/5.0' 'https://starlinkindonesia.shop/?v=YYYYMMDD' -o /tmp/starlink-root.html
! grep -Eiq 'amp-img|<img|starlinkindonesia-ksr888-logo|og:image|twitter:image' /tmp/starlink-root.html
curl -fsSI 'https://starlinkindonesia.shop/amp_ksr888_branded.html?v=YYYYMMDD'
curl -fsSI 'https://starlinkindonesia.shop/ksr888-amp-logo.png?v=YYYYMMDD'
curl -sSI 'http://starlinkindonesia.shop/' | sed -n '1,8p'
npx --yes amphtml-validator 'https://starlinkindonesia.shop/?v=YYYYMMDD'
docker compose ps app caddy
```
