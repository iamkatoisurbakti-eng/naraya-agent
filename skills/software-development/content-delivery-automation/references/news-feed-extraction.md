# News feed extraction notes

Use this as the condensed support file for news-headline and article extraction inputs that feed content pipelines.

## Pattern
- Prefer the source search/category endpoint first.
- Extract title, link, image, and article body when available.
- Fall back to page scraping if the helper API is missing or broken.
- Normalize the payload before rewriting or rendering it into a deliverable.

## Common pitfalls
- Search helpers can fail on site markup drift.
- Video/clip pages may need lighter parsing than text articles.
- Trim long article bodies before using them in captions or cards.
- Treat upstream HTTP errors as soft failures when building batches.
