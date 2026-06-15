# Nusantara AI SPA SEO audit notes

Session findings for the Nusantara AI app.

## What exists
- `web/index.html` already ships basic SEO tags:
  - title: `Nusantara AI`
  - meta description
  - `robots=index,follow`
  - OG/Twitter tags
- `web/src/components/NewsPage.tsx` updates SEO client-side:
  - `document.title`
  - canonical URL
  - `og:title`, `og:description`, `og:image`
  - `twitter:*`
- Routing includes a dedicated news subdomain/app path in `web/src/main.tsx`.

## Gaps observed
- No `robots.txt` found in repo scan.
- No `sitemap.xml` found in repo scan.
- No JSON-LD/schema markup found in the web app scan.
- Homepage H1 is brand-forward, but not keyword-forward for high-intent search.
- News article SEO is JS-set, so crawler parity may be weaker than static or prerendered pages.

## 24-hour priority order
1. Add `robots.txt` + `sitemap.xml`.
2. Add JSON-LD for `Organization`, `WebSite`, and `SoftwareApplication`.
3. Rewrite homepage title/H1/description around high-intent Indonesian keywords.
4. Create dedicated landing pages for top-intent queries.
5. Verify indexability, canonical URLs, and Open Graph images.

## Useful keyword clusters
- AI chat gratis Indonesia
- AI gambar Indonesia
- AI video generator Indonesia
- AI news automation Indonesia
- AI clipper YouTube Indonesia
- alternatif Runway / Kling / ElevenLabs Indonesia

## Verification checklist
- [ ] Home and news pages have unique titles/meta.
- [ ] Canonical URL is present on indexable pages.
- [ ] Sitemap includes home, pricing, feature pages, and news routes.
- [ ] Robots file allows indexation of public pages.
- [ ] Structured data is visible in the HTML source or prerender output.
- [ ] Main landing pages target one search intent each.
