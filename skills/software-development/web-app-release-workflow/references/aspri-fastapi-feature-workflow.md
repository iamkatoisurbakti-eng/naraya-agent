# ASPRI FastAPI Feature Workflow Notes

Use this when the repo follows the ASPRI pattern:
- FastAPI backend at `backend/main.py`
- plain HTML frontend/admin surfaces
- local PNG assets at repo root
- shared feature registry in `shared/features.json`

## Proven implementation pattern

1. Add/extend backend feature support first.
   - update feature-specific template maps in `backend/main.py`
   - keep feature fallbacks distinct (`video`, `content`, `bantu`, `bisnis`, `belajar`)
   - expose dedicated endpoints when the feature needs its own storage or workflow

2. Mirror the contract in frontend/admin HTML.
   - add controls for the new feature
   - keep feature-specific assets in the payload (`aspri-video.png`, `aspri-content.png`, etc.)
   - update metrics cards when the backend exposes new counters

3. Persist structured records under `data/`.
   - workflow jobs -> `workflow_jobs.json`
   - learning materials -> `learning_materials.json`
   - business evaluations -> `business_evaluations.json`

4. Verify with source-level checks and live HTTP.
   - `python3 -m py_compile backend/main.py`
   - `node --check` on inline frontend scripts
   - `/health`, feature endpoint, workflow/evaluation endpoint, and admin metrics

## Important pitfall

- When `uvicorn` is unavailable globally, use the project venv (`.venv/bin/uvicorn`) rather than assuming the system binary exists.
- For browser automation, Chrome profile/singleton errors can block launches even when the app is fine; treat HTTP + compile checks as the primary proof.

## Session-specific example

- ASPRI BELAJAR: 24h nonstop debate/voting/scoring, auto-add only when score > 80.
- ASPRI BISNIS: 24h multi-agent debate/backtest/validation, changes applied only when score > 80.
- ASPRI BANTU/MODUL/KEUANGAN: each uses its own evaluation storage and explicit >80 approval gate.
- ASPRI LACAK PAKET: add a separate tracking namespace/endpoints/history when the feature needs resi/status lookups; keep workflow templates and admin metrics aligned.
- Verified pattern: backend score flow can store approved records while the UI renders the evaluation history directly from API data.
