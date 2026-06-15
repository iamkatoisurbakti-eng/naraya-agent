# Homepage CTA + SPA SEO for Nusantara AI

Use this pattern when improving `nusantara-ai.online` or similar Vite/React SPA homepages for both conversion and search intent.

## What changed in this session
- Shifted homepage hero from generic branding (`Kreasi Tanpa Batas`) to intent-led copy centered on searchable commercial terms:
  - AI Chat gratis
  - AI video generator
  - image studio
  - voice agent
  - AI clipper
- Tightened CTA labels to outcome-first language:
  - `Mulai Gratis`
  - `Mulai Gratis Sekarang`
  - `Lihat Harga & Promo`
  - `Jelajahi Fitur AI`
  - `Coba Gratis Sekarang`
- Added FAQ block near footer to capture long-tail commercial questions and reduce pre-click hesitation.

## Implementation pattern for this repo
1. Update `web/index.html` for crawlable shell metadata:
   - `title`
   - `meta description`
   - `meta keywords`
   - canonical link
   - OG/Twitter tags
   - JSON-LD `SoftwareApplication`
2. Also update the landing React component so hydrated SPA navigation keeps the same SEO/copy state:
   - set `document.title`
   - patch `description`, `og:*`, `twitter:*`, and canonical in a `useEffect`
   - inject/update a stable JSON-LD script tag (for example `#landing-seo-schema`)
3. Align hero, pricing intro, and FAQ copy to the same keyword cluster and commercial intent.
4. Keep CTA copy short and direct; prefer outcome/offer language over brand-only language.

## Verification pattern
- Check live homepage HTML directly with `curl` to confirm shell metadata actually changed.
- Check the deployed JS bundle for new hydrated CTA/FAQ strings; raw HTML alone is not enough in a SPA.
- For this session, bundle verification strings included:
  - `MULAI GRATIS SEKARANG`
  - `Pertanyaan umum sebelum mulai`
  - `AI CHAT GRATIS,`
  - `Coba Gratis Sekarang`

## Pitfalls
- Updating only React copy but not `web/index.html` leaves weak crawler-visible metadata.
- Updating only `index.html` but not runtime head-sync can cause SPA navigation or hydration to drift from the intended metadata.
- Generic hero copy may look polished but underperform for search and conversion compared with intent-led copy.
