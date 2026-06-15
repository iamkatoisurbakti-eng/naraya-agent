# ASPRI feature workflow templates

Session-derived notes for ASPRI-style FastAPI + static HTML apps.

## Key pattern
When a UI lets the user choose a feature family and a template, the backend and frontend must share the same feature→template mapping.

Observed feature families:
- video: Reels / short video workflows
- content: photo-product / Instagram feed workflows
- bantu: automation workflows (WhatsApp, Instagram, voice, CRM, email)

## Working conventions
- Backend `/workflow/templates?feature=<name>` should return only templates for that feature.
- Backend `/workflow/run` should resolve the template against the selected feature, not a global default.
- Frontend/admin should populate templates from the selected feature and send the same feature value back on submit.
- Content workflows should accept user-uploaded product photos, preview them locally, and pass the chosen template plus product name to the backend.
- For content jobs, caption/CTA/hashtags should be tailored to the uploaded product/photo workflow instead of reusing video defaults.

## Verification
- `GET /health`
- `GET /workflow/templates?feature=video`
- `GET /workflow/templates?feature=content`
- `GET /workflow/templates?feature=bantu`
- `POST /workflow/run` for at least one job in each active feature family
- `python3 -m py_compile backend/main.py`
- restart the running uvicorn process after deploy so the browser sees the latest UI/backend state
