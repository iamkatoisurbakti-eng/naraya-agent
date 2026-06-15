# FastAPI + Static Web App Verification

Use this checklist when a repo has a Python backend plus static HTML/JS frontend/admin pages.

## Reliable verification sequence
1. Run backend syntax/compile checks first (for example: `python3 -m py_compile ...`).
2. Run frontend JavaScript syntax validation separately if the UI is inline or bundled.
3. Start or restart the app server after patches; stale uvicorn processes can hide fixes.
4. Smoke test live endpoints over localhost, not just unit checks.
5. Verify any persistence file changed by the new flow.
6. Re-check admin/metrics endpoints if the change adds operational counters.

## Good smoke-test targets
- `/health`
- new feature endpoint(s)
- admin metrics/dashboard endpoint
- persistence-backed list endpoint

## Common pitfalls
- Assuming compile success means runtime success.
- Forgetting to restart the server after backend edits.
- Testing only the happy path and missing persistence writes.
- Leaving frontend syntax errors untested because the page is static HTML with inline JS.

## Session note
In one ASPRI build session, a 24h learning flow was verified by:
- compile check on `backend/main.py`
- JS syntax check on `frontend/index.html`
- smoke tests for `/health`, `/learning/materials`, `/learning/evaluate`, and `/admin/metrics`
- confirming approved learning items were written to `data/learning_materials.json`

A later ASPRI session extended the same pattern to business, BANTU, and finance flows:
- `business/evaluations` and `business/evaluate`
- `bantu/evaluations` and `bantu/evaluate`
- `keuangan/evaluations` and `keuangan/evaluate` (alias `/finance/...`)
- admin metrics were expected to expose `business_*`, `bantu_*`, and `finance_*`
- a strong finance payload needed explicit cashflow, risk, audit, and numeric details to cross the `> 80` approval threshold
