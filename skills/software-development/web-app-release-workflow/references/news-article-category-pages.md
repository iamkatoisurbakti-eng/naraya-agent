# News article category pages

Use this pattern when each generated news item should also become a browsable article on the public site.

## Implementation shape
- Generate a normalized article record from each selected news seed during the news pipeline.
- Persist article files under a dedicated data root, grouped by category:
  - `data/news-articles/index.json`
  - `data/news-articles/articles/<category>/<slug>.json`
- Expose public read routes:
  - `/api/news/categories`
  - `/api/news/articles`
  - `/api/news/articles/:category/:slug`
  - `/news`
  - `/news/:category`
  - `/news/:category/:slug`
- Keep landing-page previews lightweight and point them to the internal article page when available.

## Category inference
- Use deterministic keyword/category heuristics so generated items land in a stable public category.
- Allow explicit source-based overrides for common publishers that need a single public bucket.
- Keep slugs lowercase and stable; use a readable label for display.

## Article content
- Store title, summary, excerpt, sections, source metadata, image URL, publishedAt, createdAt, and internal article URL.
- Reuse the original source link as a fallback CTA when no internal article page is available.
- Prefer a short, SEO-friendly article body with a few sections instead of dumping raw source text.

## Pitfalls
- Do not rely on build output as the source of truth; persist article files under `data/news-articles`.
- When adding category pages, update both API routes and SPA routes together so the public URL actually resolves.
- If the landing widget links to internal articles, preserve the original external URL as a fallback.
- Category inference should be deterministic; if a source is meant to live in one bucket, codify that override rather than hoping the keyword matcher picks it.

## Verification
- Generate one news item and confirm these files exist:
  - `data/news-articles/index.json`
  - `data/news-articles/articles/<category>/<slug>.json`
- Fetch `/api/news/categories` and `/api/news/articles?category=<slug>`.
- Open `/news/<category>/<slug>` and verify the detail page renders.
- Grep the landing bundle for the new `News` link if the public nav changed.
