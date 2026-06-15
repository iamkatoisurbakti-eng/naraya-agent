# Google Search Console OAuth + 24h SEO loop notes

Use when a user wants a live site monitored/backtested for Google index readiness and Search Console integration.

## Key lessons
- Search Console indexing cannot be guaranteed by an agent. Phrase results as crawl/index-readiness unless the Search Console API returns a verified status.
- A Google Cloud service account JSON can authenticate, but Search Console UI may reject the service-account email with “email tidak ditemukan” or the API may return an empty `sites` list. In that case, use OAuth with the user’s real Google account that owns the GSC property.
- If the user provides an OAuth client JSON and it is `web` type rather than `installed`/Desktop, add a redirect URI in Google Cloud before starting auth:
  - `http://localhost:1/`
- After approval, the browser will fail on localhost; that is expected. Ask the user to paste the full redirected URL from the address bar.
- For OAuth Desktop/installed clients in a headless CLI, persist the PKCE `code_verifier` alongside the generated auth URL. If exchange fails with `Missing code verifier`, patch the setup helper to save and restore it, then generate a fresh auth URL because old codes are one-time use.
- If exchange fails because returned scopes include stale/extra scopes from previous grants, regenerate the auth URL with `include_granted_scopes=false` and ask the user to authorize again. Do not reuse old redirect URLs.
- For localhost HTTP redirects, set `OAUTHLIB_INSECURE_TRANSPORT=1` only for the token exchange command.
- Keep OAuth client/token files under a local `secrets/` directory with `chmod 600`; never echo client secrets/private keys.

## Starlink-specific implementation from this session
- Credential paths used:
  - Service account: `/root/nusantara-ai-saas/secrets/starlink-gsc-service-account.json`
  - OAuth client: `/root/nusantara-ai-saas/secrets/starlink-gsc-oauth-client.json`
  - OAuth token target: `/root/nusantara-ai-saas/secrets/starlink-gsc-oauth-token.json`
- Helper scripts created:
  - `scripts/gsc_starlink_check.py` now prefers OAuth token when present, then checks Search Console property access, sitemap, and URL Inspection for the 4 focus URLs.
  - `scripts/gsc_oauth_setup.py` generates an OAuth URL, stores PKCE pending state/verifier, exchanges the redirected code/URL, and checks Search Console access.
- Verified OAuth result from this session:
  - Property: `sc-domain:starlinkindonesia.shop`
  - Permission: `siteOwner`
  - Sitemap: `https://starlinkindonesia.shop/sitemap.xml`, downloaded, `warnings=0`, `errors=0`
  - URL Inspection baseline: root `Crawled - currently not indexed`; `/ksr888`, `/situs-terpercaya`, and `/situs-slot-gacor` `Discovered - currently not indexed`.
- If GSC API shows `site_not_found_or_no_permission`, instruct the user to use OAuth or verify the property owner account. Do not keep retrying the same service-account flow.

## 24h loop guardrails
- Each iteration should check: HTTPS 200, robots, sitemap, no `noindex`, self canonical, title/meta/H1, FAQ/WebSite/Organization/Breadcrumb schema, AMP validity, and page size/performance.
- Run a short A/B debate before editing. Only deploy if the improvement is clear, safe, and not keyword stuffing.
- Preserve user performance choices: if the user removed heavy logos/images, do not reintroduce `amp-img`, `<img>`, `og:image`, `twitter:image`, or manifest icons unless explicitly asked.
- Avoid black-hat SEO, cloaking, fake ratings, backlink spam, and false gambling claims such as “pasti menang” or “jackpot dijamin.”
