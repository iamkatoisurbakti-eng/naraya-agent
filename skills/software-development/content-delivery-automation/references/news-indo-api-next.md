# Berita Indo API Next: session notes

Base URL:
- https://berita-indo-api-next.vercel.app

Discovery endpoint:
- GET /api returns the route map for all providers.

Useful routes observed in session:
- /api/cnn-news/:type
  - types: nasional, internasional, ekonomi, olahraga, teknologi, hiburan, gaya-hidup
- /api/cnbc-news/:type
  - types: market, news, entrepreneur, syariah, tech, lifestyle
- /api/republika-news/:type
- /api/tempo-news/:type
  - types include nasional, bisnis, metro, dunia, bola, sport, cantik, tekno, otomotif, nusantara
- /api/antara-news/:type
  - types include terkini, top-news, ekonomi, lifestyle, hiburan, tekno, otomotif, rilis-pers
- /api/okezone-news
- /api/kumparan-news
- /api/tribun-news
- /api/zetizen-jawapos-news
- /api/suara-news
- /api/vice-news
- /api/voa-news

Observed payload shapes:
- CNN/CNBC/Kumparan/Okezone/Antara items usually expose title, link, summary/content fields, isoDate/pubDate, and image or image object.
- Some images are nested objects with small/medium/large fields.

Selection/filter notes:
- The API may return off-topic or undesirable items; keep a deny-list for religion, politics, and sexual content.
- A freshness+visual-punch rank works well: image present, published time present, title contains viral/tech/lifestyle/travel/gaming/fashion/food cues.
- Deduplicate by normalized title and/or title+link.

Rendering notes:
- In this session, /root/template.html was the working HTML card template with a #news-card root.
- /root/genz.html was a separate spec-like HTML file and did not contain #news-card; using it directly caused Playwright waits to time out.
- If a user names a template, verify the actual DOM anchor before wiring the screenshot step.

CLI probe that worked:
- urllib.request.urlopen(url, timeout=20) against the API was enough to inspect routes and sample payloads.
- Browser navigation to the site homepage timed out in this environment, so direct HTTP fetch was the reliable inspection path.
