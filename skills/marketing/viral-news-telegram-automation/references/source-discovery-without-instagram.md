# Source discovery without Instagram access

Session note: direct access to public Instagram profile pages is often login-gated or returns 429/timeouts, so the reliable fallback for trend curation is to read the publisher sites directly.

## Practical fallback order
1. **Kumparan**
   - Use `https://kumparan.com/robots.txt` to discover sitemap URLs.
   - Latest news items are available in channel sitemaps such as:
     - `https://kumparan.com/sitemap_channel_news.xml`
     - `https://kumparan.com/sitemap_channel_entertainment.xml`
     - `https://kumparan.com/sitemap_channel_tekno-sains.xml`
   - Each `<url>` block includes `news:title`, `loc`, and timestamp.

2. **USS Feed**
   - Use `https://ussfeed.com/sitemap_index.xml` and the newest `post-sitemap*.xml` files.
   - The main site also exposes recent editorial links on the homepage.

3. **Infipop**
   - The homepage exposes usable article/event links directly.
   - `https://infipop.id/robots.txt` exists, but sitemap endpoints were not available in this session.

## Extraction notes
- Prefer article/page metadata (`og:title`, `og:description`, first substantive paragraph) over social-platform summaries when available.
- For ranking, prioritize freshness, shareability, and clean one-line headlines.
- If the user asks for “latest from @kumparan/@infipop.id/@ussfeeds”, treat that as a source brand request, not a requirement to scrape Instagram itself.

## Pitfalls
- Do not block on Instagram profile HTML if the page redirects to login or returns 429.
- Do not invent post contents from profile names alone.
- Do not expose source labels in the public deliverable.
