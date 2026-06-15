# Starlink AMP logo removal + GSC readiness loop

Use when maintaining `starlinkindonesia.shop` static/AMP landing pages for SEO/indexing and performance.

## Context
- Repo: `/root/nusantara-ai-saas`
- Host routing: `src/app.ts` serves `starlinkindonesia.shop` and `www.starlinkindonesia.shop` from static files in `web/public/`.
- Main files:
  - `web/public/amp_ksr888_branded.html`
  - `web/public/starlinkindonesia.html`
  - `web/public/ksr888.html`
  - `web/public/situs-terpercaya.html`
  - `web/public/situs-slot-gacor.html`
  - `web/public/manifest.webmanifest`

## Performance correction from session
The user explicitly requested removing the heavy logo because it lowered performance. Do not re-add the PNG/logo to the Starlink AMP pages unless the user explicitly reverses this.

Remove/avoid:
- `<amp-img ... starlinkindonesia-ksr888-logo ...>`
- raw `<img>` logo tags
- `starlinkindonesia-ksr888-logo` references in HTML
- `og:image` and `twitter:image` pointing to the heavy logo
- `Organization.logo` JSON-LD field for the heavy logo
- manifest icons pointing to the heavy logo

Use instead:
- Text brand marker: `<div class="ksr-brand" aria-label="KSR888">KSR888</div>`
- Lightweight CSS for `.ksr-brand`

## Verification commands
```bash
cd /root/nusantara-ai-saas
npm run build
bash scripts/deploy.sh

TMP=/tmp/starlink-nologo.html
curl -fsS -A 'Mozilla/5.0' 'https://starlinkindonesia.shop/?v=nologo-check' -o "$TMP"
! grep -Eiq 'amp-img|<img|starlinkindonesia-ksr888-logo|og:image|twitter:image' "$TMP"

for p in /ksr888 /situs-terpercaya /situs-slot-gacor; do
  curl -fsS -A 'Mozilla/5.0' "https://starlinkindonesia.shop$p?v=nologo-check" -o /tmp/p.html
  ! grep -Eiq 'amp-img|<img|starlinkindonesia-ksr888-logo|og:image|twitter:image' /tmp/p.html
done

npx --yes amphtml-validator \
  'https://starlinkindonesia.shop/?v=nologo-check' \
  'https://starlinkindonesia.shop/ksr888?v=nologo-check' \
  'https://starlinkindonesia.shop/situs-terpercaya?v=nologo-check' \
  'https://starlinkindonesia.shop/situs-slot-gacor?v=nologo-check'

docker compose ps app caddy
```

## GSC loop notes
A 24h cron loop may monitor Google Search Console readiness, but direct Google indexing cannot be claimed without verified GSC credentials/API output. Each run should:
- Check whether GSC credentials exist.
- Fetch root/support pages, robots, sitemap with Googlebot-like UA.
- Verify HTTPS 200, no `noindex`, self canonical, sitemap includes the 4 focused URLs, robots allows search crawl, AMP validator PASS, schema/title/meta/H1 present.
- Run A/B debate and only patch low-risk improvements.
- Keep responsible-play copy and avoid false claims like guaranteed winning/jackpot.
- Preserve the no-logo performance constraint above.
