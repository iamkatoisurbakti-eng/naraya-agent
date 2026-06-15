# ASPRI Feature-Family Workflow Notes

Use this reference for the ASPRI Nusantara app family when shipping FastAPI-backed HTML admin/frontend changes with local assets and feature-specific evaluation endpoints.

## Observed app shape

- Backend: `backend/main.py`
- Frontend: `frontend/index.html`
- Admin: `admin/index.html`
- Shared feature registry: `shared/features.json`
- Local assets: PNGs under the repo root or `/assets`
- Runtime port: `8090`
- Local server launch: `.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8090`

## Verification order that worked

1. Compile backend before touching runtime:
   - `python3 -m py_compile backend/main.py`
2. Check frontend script syntax when logic lives in inline JS:
   - `node --check` on extracted `<script>` blocks
3. Restart the app with the repo venv, not system uvicorn:
   - use `.venv/bin/uvicorn` if global `uvicorn` is missing
4. Smoke test the health and feature endpoints immediately after restart:
   - `/health`
   - workflow templates/run
   - domain-specific evaluation endpoints such as `/learning/evaluate`, `/business/evaluate`, `/bantu/evaluate`
5. Verify the admin metrics endpoint reflects new counters after the patch.

## Feature-family patterns

- `video`, `content`, `bantu`, `design`, `pos`, and `lacak` can share a generic workflow runner but need feature-specific templates/assets and fallback prompts.
- `content` is easier to maintain as its own feature namespace when it has upload/preview/template UI.
- `belajar`, `bisnis`, and `bantu` each benefited from their own evaluation endpoints and storage files.
- Approval gates should be explicit in both backend and UI. In this app family, approved outputs are applied only when score > 80.

## Pitfalls

- Do not assume system `uvicorn` exists; use the repo venv.
- Do not treat a successful compile as sufficient; restart and hit the live endpoint.
- If the frontend is static HTML, syntax errors in inline JS can break the app even when backend tests pass.
- Keep admin/dashboard counters in sync with new evaluation storage files.
- Avoid surfacing internal scoring jargon to users unless the UI is explicitly for evaluation/debugging.

## Session-specific detail worth reusing

- BANTU was extended with a 24h multi-agent evaluation flow for new feature requests; features are added only when the score is above 80.
- Learning materials and business evaluations were stored separately so each workflow could be verified and queried independently.
- A restart after deploy was needed for changes to show up immediately.
