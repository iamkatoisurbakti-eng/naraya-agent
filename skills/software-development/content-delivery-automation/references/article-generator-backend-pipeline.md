# Article Generator backend pipeline notes

This repo now has a safe article-generation path for content pipelines that read a feed or text, call the external Article Generator API, and save drafts locally.

Key facts:
- External API base: `https://use.api.co.id/article-generator`
- Auth header: `x-api-co-id`
- Recommended env vars:
  - `ARTICLE_GENERATOR_API_KEY`
  - `ARTICLE_GENERATOR_BASE_URL`
- Backend should keep the key server-side only; never expose it in responses, logs, or client bundles.
- Safe backend surface added in the repo:
  - `GET /api/admin/article-generator/status`
  - `GET /api/admin/article-generator/drafts`
  - `POST /api/admin/article-generator/draft`
- Drafts are saved under `data/article-drafts/` as JSON + HTML.

Workflow notes from the session:
- Feed intake should normalize title, summary, URL, and keywords before generation.
- Reject non-public rewrite URLs. Block `localhost`, `.local`, private RFC1918 ranges, and non-http(s) schemes.
- For TSX cron/job scripts in this repo, load `.env.production` first, then `.env` as a fallback.
- For admin auth tests, it was more reliable to mint a JWT directly with `signAccessToken` than to depend on email-based admin config in the test fixture.
- A job can be scheduled as a cron task that runs a single coordinator script and delegates the substeps conceptually: feed intake, draft generation, QA.

Useful command:
- `npm run gen:article-generator-feed-job`

Related repo files:
- `src/services/article-generator.ts`
- `src/services/article-drafts.ts`
- `src/routes/admin.ts`
- `scripts/article-generator-feed-job.ts`
