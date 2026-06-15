# Starlink AMP SEO 24h loop

Use when running or updating the 24-hour multi-agent SEO/indexing loop for `starlinkindonesia.shop`.

## Current target
- Domain: `https://starlinkindonesia.shop/`
- Keywords: `KSR888`, `Situs Terpercaya`, `Situs Slot Gacor`
- Focus URLs:
  - `/`
  - `/ksr888`
  - `/situs-terpercaya`
  - `/situs-slot-gacor`

## Loop behavior
Each run should coordinate subagents for:
1. Google Search Console/indexability audit.
2. On-page SEO and CTR audit.
3. Live technical/performance verification.

Checks:
- Googlebot and browser-like HTTP 200 for all focus URLs, `robots.txt`, `sitemap.xml`.
- No `noindex`; self canonical per page.
- Sitemap contains the 4 focused URLs only for Starlink host.
- AMP validator passes for all 4 routes.
- FAQ/WebSite/Organization/Breadcrumb schema present.
- Title/meta/H1 include target keywords naturally.
- Responsible-play language remains; no guaranteed win/jackpot claims.
- No heavy logo/image regression: root/support HTML must not contain `amp-img`, `<img`, `starlinkindonesia-ksr888-logo`, `og:image`, or `twitter:image` unless the user explicitly reverses the no-logo performance request.

## Google Search Console API setup/status
- Preferred working auth for this host is OAuth Desktop App, not service account. Search Console UI may reject service-account emails as “not found”.
- OAuth client/token files:
  - `/root/nusantara-ai-saas/secrets/starlink-gsc-oauth-client.json`
  - `/root/nusantara-ai-saas/secrets/starlink-gsc-oauth-token.json`
  - mode should be `600`; never print token/client secret/private key contents.
- OAuth helper: `python3 scripts/gsc_oauth_setup.py`.
  - `--auth-url` creates a localhost redirect URL and stores PKCE pending state/verifier.
  - `--auth-code '<full redirected localhost URL>'` exchanges the code. Use `OAUTHLIB_INSECURE_TRANSPORT=1` for the localhost HTTP redirect.
  - If Google returns extra old scopes and exchange fails, regenerate auth URL with `include_granted_scopes=false` and ask the user to login again; OAuth codes are one-time use.
- GSC check helper: `python3 scripts/gsc_starlink_check.py`.
  - It should prefer OAuth token when present, then list accessible properties, check sitemap status, and run URL Inspection for the 4 focus URLs.
- Verified baseline from this session:
  - property `sc-domain:starlinkindonesia.shop` accessible as `siteOwner` via OAuth.
  - sitemap `https://starlinkindonesia.shop/sitemap.xml` submitted/downloaded with `warnings=0`, `errors=0`.
  - URL Inspection: root was `Crawled - currently not indexed`; support pages were `Discovered - currently not indexed`.
- Service account fallback exists at `/root/nusantara-ai-saas/secrets/starlink-gsc-service-account.json`, email `starlinkindonesia-gsc-agent@teak-clone-494608-s1.iam.gserviceaccount.com`, but OAuth is the known-good path here.

## Google Search Console caveat
Do not claim indexing was achieved or sitemap/URL inspection was submitted unless verified by GSC API/tool output. GSC URL Inspection can monitor normal pages but does not force general web-page indexing. Keep the site crawl-ready and report real coverage states such as `Crawled - currently not indexed` honestly.

## Safe update rule
Run a short A/B debate before editing:
- A: keep current live.
- B: proposed improvement.
Only edit/deploy when B clearly improves score, is low-risk, avoids keyword stuffing, and preserves AMP validity/performance.

## Verification snippet
```bash
cd /root/nusantara-ai-saas
for p in / /ksr888 /situs-terpercaya /situs-slot-gacor /sitemap.xml /robots.txt; do
  curl -L -s -o /dev/null -w "$p %{http_code}\n" \
    -A 'Googlebot/2.1 (+http://www.google.com/bot.html)' \
    "https://starlinkindonesia.shop$p?v=gsc-check"
done

TMP=/tmp/starlink-gsc-check.html
curl -fsS -A 'Mozilla/5.0' 'https://starlinkindonesia.shop/?v=gsc-check' -o "$TMP"
! grep -Eiq 'amp-img|<img|starlinkindonesia-ksr888-logo|og:image|twitter:image' "$TMP"

python3 scripts/gsc_oauth_setup.py --check
python3 scripts/gsc_starlink_check.py

npx --yes amphtml-validator \
  'https://starlinkindonesia.shop/?v=gsc-check' \
  'https://starlinkindonesia.shop/ksr888?v=gsc-check' \
  'https://starlinkindonesia.shop/situs-terpercaya?v=gsc-check' \
  'https://starlinkindonesia.shop/situs-slot-gacor?v=gsc-check'
```
