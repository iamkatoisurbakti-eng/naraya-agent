# Live SEO A/B Looping Notes

Use this when backtesting a live landing page over 24h and comparing variants before changing production.

## Pattern
1. Fetch live HTML and headers for the target host and the main entry routes.
2. Inspect title, meta description, canonical, H1, OG, Twitter, JSON-LD, and robots/sitemap presence.
3. Score the current page vs an improved variant using the same rubric.
4. Run a short A/B debate:
   - A = keep current live
   - B = apply the stronger SEO variant
5. Vote and pick the winner.
6. Only apply changes when the winning variant is clearly better and the score is above the user-approved threshold.
7. Re-run the same checks after deploy and again at the next review interval.

## Evidence to collect
- `curl -I` headers
- raw HTML snippets from root, mobile, and desktop routes
- presence/absence of canonical, OG, Twitter, JSON-LD
- H1 visibility and copy intent
- robots.txt and sitemap.xml accessibility

## Scoring cues
- Technical SEO: indexability, canonical correctness, sitemap/robots, schema
- On-page SEO: title/meta/H1 alignment, keyword intent, duplication
- UX/readability: copy clarity, hierarchy, mobile fit
- Trust/brand: brand clarity, visual consistency, confidence signals
- Conversion readiness: CTA clarity, friction, intent match
- Performance/caching: cache behavior, TTFB hints, no-store/no-cache issues

## Common pitfall
A live page can look improved in source while the deployed host still serves stale HTML. Always verify the live host after build/deploy or proxy/cache refresh.