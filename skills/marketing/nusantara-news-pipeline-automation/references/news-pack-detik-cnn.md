# Detik + CNN news-pack workflow

Use this reference when the user asks for a compact daily news pack from Detik and CNN Indonesia, then wants one chosen story rewritten into Instagram caption, Canva flyer copy/prompt, and a 30-second video script.

## Source pull pattern

Preferred sources and routes observed in this session:

CNN Indonesia
- RSS endpoints worked reliably:
  - `https://www.cnnindonesia.com/teknologi/rss`
  - `https://www.cnnindonesia.com/ekonomi/rss`
  - `https://www.cnnindonesia.com/olahraga/rss`
  - `https://www.cnnindonesia.com/hiburan/rss`
- RSS items expose `title`, `link`, `description`, and `pubDate`.
- Category feed pages also work if RSS is unavailable, but RSS is cleaner for recent-item ranking.

Detik
- Detik category home pages were usable for candidate discovery:
  - `https://inet.detik.com/`
  - `https://finance.detik.com/`
  - `https://sport.detik.com/`
  - `https://hot.detik.com/`
- Article candidates often appear in anchors with `dtr-ttl` and `href`.
- For article detail text, `og:title`, `og:description`, and the article body under `div.detail__body-text` are useful fallbacks.
- The helper/API workflow can fail or be awkward; direct page parsing is a valid fallback.

## Filtering rule

Only keep stories in these buckets:
- Teknologi & AI
- Bisnis & Ekonomi
- Olahraga
- Hiburan

Discard anything outside those buckets even if it is recent.

## Selection heuristic for “paling menarik/viral”

Choose the item with the best blend of:
- recency
- broad audience recognition
- clear hook in one sentence
- visual/event-scene potential for flyer/video
- easy CTA angle for Gen Z readers

If multiple candidates are close, prefer the one with:
1. a familiar brand/person/team
2. a strong surprise or consequence angle
3. a simple summary that can be told in 20–30 seconds

## Output contract for the chosen story

Use exactly these three blocks:

OUTPUT A: CAPTION INSTAGRAM
- one hook line
- 3–4 sentence summary in casual but informative Indonesian
- 5–7 relevant hashtags
- short CTA

OUTPUT B: JUDUL + PROMPT CANVA
- flyer title max 8 words
- one short subtitle
- 4:5 Canva prompt with dominant colors, font style, and suggested visual elements

OUTPUT C: SCRIPT VIDEO 30 DETIK
- 0–3 detik: hook
- 3–20 detik: main points
- 20–27 detik: context/dampak
- 27–30 detik: closing + CTA

## Tone notes

- Keep it santai but informative.
- Gen Z feel is fine, but do not make the wording sloppy.
- Do not over-explain the source selection unless the user asks.
- Keep visible public-output copy source-label free unless the user explicitly wants source labels.
