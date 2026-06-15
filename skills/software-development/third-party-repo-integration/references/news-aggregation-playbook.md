# News Aggregation Integration Notes

Session context: ASPRI BERITA integrated three external news sources into a FastAPI host app.

## Providers and quirks
- API Berita Indonesia:
  - live endpoint pattern: `/SOURCE/CATEGORY` (e.g. `/cnn/terbaru`)
  - in this session it returned HTTP 402 for live fetches, so the host app must not treat non-2xx as fatal.
- Berita Indo API:
  - endpoint pattern: `/api/<feed>` (e.g. `/api/cnn-news`)
  - payload shapes vary; use recursive extraction and normalize items before rendering.
- Detik Search API (via `dn_scraper`):
  - optional dependency, not always installed in the runtime
  - when missing, return a local fallback digest instead of failing the request.

## Recommended host behavior
- Expose a provider catalog endpoint so the UI can populate provider/source/category selectors.
- Normalize feed items into one common shape:
  - title
  - link
  - image
  - published_at
  - summary
  - source
  - provider
  - feed_source
  - category
- Deduplicate on title+link.
- If remote fetch fails, return a local fallback digest with safe placeholder links so the UI stays usable.
- Keep the workflow surface separate from the news surface; news is a dedicated module, not just a workflow template.

## Verification recipe
1. Restart the FastAPI app after code changes.
2. Check health:
   - `curl http://127.0.0.1:8090/health`
3. Check provider catalog:
   - `curl http://127.0.0.1:8090/news/providers`
4. Check feed fallback behavior:
   - `curl 'http://127.0.0.1:8090/news/feed?provider=api-berita-indonesia&source=cnn&category=terbaru&limit=2'`
   - `curl 'http://127.0.0.1:8090/news/feed?provider=detik&source=search&query=ekonomi&limit=2'`

## Pitfalls
- Treating provider HTTP errors as app failures.
- Assuming every upstream returns the same JSON shape.
- Forgetting to add a local fallback path for the UI.
- Launching the UI before the backend endpoints exist.
