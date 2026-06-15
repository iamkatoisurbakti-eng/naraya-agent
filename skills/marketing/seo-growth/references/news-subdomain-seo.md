# Nusantara-AI News subdomain SEO checklist

Use this when working on `news.nusantara-ai.online`.

## What matters most
- SPA shell metadata alone is not enough for crawlability.
- Serve `robots.txt` and `sitemap.xml` from the news host itself.
- Include index page, category pages, and article detail URLs in sitemap.
- Apply route-aware meta tags for article/category pages after client load.
- Verify the public host after deploy, not just local build output.

## Practical implementation notes
- `robots.txt` should allow crawling and point to `/sitemap.xml`.
- `sitemap.xml` should list:
  - `/news`
  - `/news/<category>`
  - `/news/<category>/<slug>`
  with `lastmod` where available.
- Article pages should set:
  - title
  - meta description
  - canonical URL
  - OG and Twitter tags
- If article data lives in a generated JSON index, ensure the production container has synced data before testing public URLs.

## Verification commands
```bash
curl -fsS https://news.nusantara-ai.online/robots.txt
curl -fsS https://news.nusantara-ai.online/sitemap.xml | sed -n '1,40p'
curl -fsSI https://news.nusantara-ai.online/news/<category>/<slug>
```

## Common pitfall
- Building only `web/index.html` metadata and skipping route-aware tags leaves article detail pages under-optimized for crawlers and social previews.
