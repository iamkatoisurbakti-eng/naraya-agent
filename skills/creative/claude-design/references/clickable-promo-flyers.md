# Clickable promo flyers and ad-size delivery

Use this when the user asks for promo flyers, ad banners, or social creatives that should also drive direct clicks.

## Core rule
PNG/JPG exports are not clickable assets by themselves.

If the user asks to "make the CTA clickable":
- keep generating the normal raster export (`.png`) for ad upload
- also generate a clickable wrapper (`.html`) with the same design language and a real anchor CTA
- if helpful, generate an editable `.svg` whose CTA area and footer URL are wrapped in links for browser-capable viewers
- state the limitation plainly: clickable behavior lives in HTML/SVG-in-browser, not in the PNG file

## Practical delivery set
For one finished creative, prefer shipping all three:
1. `name.png` — upload-ready raster
2. `name.html` — clickable landing-style wrapper or fullscreen creative
3. `name.svg` — editable source, optionally link-wrapped

## Local-tool fallback workflow
When image-model tooling is unavailable:
1. design the creative locally as SVG or self-contained HTML
2. export a PNG with local tools (for example `ffmpeg` + `librsvg`)
3. keep the SVG as the editable source of truth
4. if the user wants direct clicks, add the HTML wrapper instead of pretending the PNG can do it

## Ad-size pattern learned in this session
For promo checkout campaigns, the common trio is:
- `1080x1350` for portrait/social feed
- `1080x1080` for square placements
- `1920x1080` for display/banner or fullscreen desktop placement

## Copy/layout guidance for hard-selling variants
When the user asks for a more sales/hard-selling version:
- make the hook more direct (`PASANG ... LEBIH HEMAT`, `PROMO TERBATAS`, `AMBIL PROMO SEKARANG`)
- keep the offer and price dominant above the fold
- add 2–3 short buying reasons only (discount, payment ease, checkout speed)
- keep the final offer, URL, and CTA stable across variants so performance differences are attributable to the hook/layout

## Brand-reference guardrail
If the user asks for a theme similar to a known brand (for example Starlink), borrow the posture:
- dark minimal palette
- strong contrast
- premium spacing
- restrained cool-blue accent

Do not claim or imply official branding ownership unless the user explicitly has rights.
