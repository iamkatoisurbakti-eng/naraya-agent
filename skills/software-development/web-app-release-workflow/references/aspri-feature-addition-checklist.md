# ASPRI Feature Addition Checklist

Use this checklist when adding a new ASPRI feature to the FastAPI + plain HTML app family.

## Stable pattern for a new feature

1. Add backend support first in `backend/main.py`.
   - create or extend the feature template map
   - add a dedicated fallback in `local_answer(feature=...)`
   - add a dedicated endpoint if the feature needs its own storage or evaluation history

2. Mirror the contract in the frontend.
   - add a home card or screen in `frontend/index.html`
   - wire the feature into the workflow selector and/or direct action button
   - pass the correct local asset payload for the feature

3. Keep admin aligned.
   - add the feature option in `admin/index.html`
   - add any new metrics cards exposed by the backend
   - keep workflow template labels consistent across UI surfaces

4. Persist records under `data/` when the feature has state.
   - examples: learning materials, business evaluations, feature requests, finance evaluations, module evaluations, invoices, tracking history

## Verification sequence that worked well

- `python3 -m py_compile backend/main.py`
- `node --check` on inline frontend/admin scripts
- restart with `.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8090`
- if port 8090 is busy, stop the old listener PID before restarting
- smoke test `/health`, the feature endpoint, workflow template/run, and admin metrics

## Recent ASPRI examples

- `content`: upload/preview UI plus template selector for social content
- `belajar`: 24h debate/voting/scoring with auto-add only when score > 80
- `bisnis`: 24h multi-agent debate/backtest/validation with change approval only when score > 80
- `bantu`: 24h feature-request evaluation with approval gating above 80
- `keuangan` and `modul`: their own evaluation histories and approval gates above 80
- `pos`: invoice, paid/unpaid state, and revenue metrics
- `design`: brand kit / promo / logo brief flow
- `lacak`: package tracking history with ETA/timeline output
- `ide-bisnis`: business idea, market validation, pricing, and launch-plan flow
