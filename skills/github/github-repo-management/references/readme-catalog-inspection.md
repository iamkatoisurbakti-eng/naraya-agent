# README catalog inspection

Use this when a cloned repository is mainly a documentation/catalog index rather than source code.

Workflow:
1. Shallow-clone the repo if you only need the catalog content.
2. Identify the heading for the category you want with `read_file` or `rg`.
3. Read only the nearby lines around that heading; table rows are usually the source of truth.
4. Prefer the repo's README over mirrors, blog posts, or stale issue comments.
5. Summarize only the matching rows, including auth and status if present.

Example from `api-publik/indonesia`:
- Category heading: `### Berita`
- Relevant rows: news APIs such as `Detik News API`, `Berita Indo API`, `CNN Indonesia`
- For multi-source scraping, prefer RSS/aggregator-style entries over single-publisher endpoints.
