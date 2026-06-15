# Admin article draft editor pattern

Context:
- Repo: /root/nusantara-ai-saas
- Feature: article-generator drafts surfaced in the admin dashboard
- Goal: list, search, inspect, and edit stored drafts from the web UI

Backend pattern:
- Admin-only endpoints:
  - GET /api/admin/article-generator/status
  - GET /api/admin/article-generator/drafts?limit=30
  - PATCH /api/admin/article-generator/drafts/:id
- Keep edit payloads whitelist-only.
- Keep `id` and `slug` immutable in the edit flow.
- Persist updates back to:
  - per-draft JSON file
  - per-draft HTML file
  - index.json for the list view

Frontend pattern:
- Add a compact split view inside the existing admin dashboard:
  - left: searchable draft list
  - right: selected draft editor
- Keep one selected draft in state and a separate form state.
- Use polling for list/status refresh, but do not overwrite the editor while the user is editing.
- Use a ref for the selected draft id when periodic refreshes run.

Useful UI fields:
- title
- summary
- html
- keywords
- sourceUrl
- feedText
- imageUrl
- responseMode
- meta fields

Pitfalls:
- Polling can reset the current edit if you rebuild form state from a stale selected id.
- PATCH support is needed in the client API helper, not just POST/GET.
- If the admin page already has heavy live polling, keep the draft editor refresh lightweight.
- Always verify with both API tests and a production frontend build.
