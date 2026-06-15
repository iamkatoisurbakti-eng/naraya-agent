# ASPRI Feature-Family Workflow Debugging

Use this reference for ASPRI / Nusantara-style apps where one backend powers multiple feature families such as `video` and `bantu` and the frontend/admin must switch template sets dynamically.

## What changed in this session

- Backend template families live in `backend/main.py`.
- `video` and `bantu` need separate template families and result copy.
- Frontend and admin must both let the user choose a feature first, then show the matching template list.
- The backend should resolve the requested template from the selected feature, not from a global video-only list.

## Update pattern

When adding a new workflow family or template:

1. Update backend template maps first.
   - Add the template under the matching feature family.
   - Make sure `/workflow/templates?feature=<name>` returns that family.
   - Make `/workflow/run` resolve from the selected feature family.

2. Update every UI surface that hardcodes template options.
   - Frontend feature selector.
   - Admin feature selector.
   - Any module card or label that describes the feature.
   - Any fallback template list in JS.

3. Keep feature-specific result copy consistent.
   - `video` can keep video-oriented captions/hashtags/CTA.
   - `bantu` should use automation-oriented copy such as autoreply, DM routing, or admin handoff.

4. Verify the runtime contract, not just the HTML.
   - `GET /workflow/templates?feature=video`
   - `GET /workflow/templates?feature=bantu`
   - `POST /workflow/run` for each feature
   - confirm the returned `job.result` matches the selected family

## Known pitfalls

- A feature selector can look correct in the UI while the backend still uses a stale global template list.
- If one surface changes and the other does not, users will see mismatched options between frontend and admin.
- The fallback `caption`, `hashtags`, and `cta` fields should be set per feature if the consumer UI surfaces them.
- The live server in this repo may be running from `.venv/bin/uvicorn`; the system `python -m uvicorn` path can fail if uvicorn is not installed globally.

## Verification commands

```bash
python3 -m py_compile backend/main.py
fuser -n tcp 8090
./.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8090
```

Then smoke test:

```bash
curl -sS http://127.0.0.1:8090/health
curl -sS 'http://127.0.0.1:8090/workflow/templates?feature=video'
curl -sS 'http://127.0.0.1:8090/workflow/templates?feature=bantu'
curl -sS -X POST http://127.0.0.1:8090/workflow/run \
  -H 'Content-Type: application/json' \
  -d '{"feature":"bantu","template":"ig-autoreply","prompt":"Balas DM harga paket","user_id":"smoke"}'
```

## UI notes from this session

- The public frontend workflow card now uses a feature selector plus a template selector.
- The admin workflow panel now uses the same pattern.
- BANTU now includes `Autoreply Instagram` alongside WhatsApp/voice/CRM/email templates.
- The module label for ASPRI BANTU should describe the feature family, not only WhatsApp.
