# News integration notes

Use this pattern when adding a read-only news feed to a React + Express app.

## Backend
- Add a dedicated route, e.g. `/api/news`, that proxies the third-party feed and normalizes article fields.
- Keep the upstream base URL in config/env, not hardcoded in the route.
- Normalize to a stable shape:
  - `id`, `title`, `summary`, `url`, `imageUrl`, `source`, `sourceKey`, `category`, `author`, `publishedAt`
- Support:
  - `source=all` for multi-source aggregation
  - per-source filtering
  - `search` and `limit`
- Return a safe response even if some sources fail: include `errors`/`sourceErrors` instead of failing the entire request.

## Frontend
- Add a dedicated dashboard section rather than overloading an unrelated studio panel.
- Provide controls for source, search, and limit.
- Show cards with image, title, summary, source badge, category, and an outbound link.

## Verification
- Add a targeted API test that mocks `fetch` and checks normalization.
- Run the app typecheck before broad test suites; new dashboard sections often surface unrelated TS narrowing issues.
- If the project uses separate frontend/backend tsconfig files, a green `tsc -p web/tsconfig.json` is a strong signal that the new section wiring is safe.

## Pitfalls
- Avoid leaking upstream provider URLs or keys in the client bundle.
- Prefer feature labels like `News Indo` / `Multi-Sumber` over raw provider names in the UI.
- Do not treat `source=all` as a single API source; it should merge multiple feeds and dedupe by stable content/url hash when possible.
