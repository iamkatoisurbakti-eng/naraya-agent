# ASPRI Design Evaluation

Use this reference for ASPRI DESIGN changes in `/root/nusantara-agent/aspri-nusantara-app`.

## Purpose

ASPRI DESIGN now has a dedicated 24h multi-agent review flow for design briefs and outputs.

## Endpoints

- `GET /design/evaluations`
- `POST /design/evaluate`
- `GET /workflow/templates?feature=design`
- `POST /feature/design`

## Evaluation shape

- planner / critic / validator / backtest voting
- loop scoring from 1–5 iterations
- final approval rule: `score > 80` plus majority yes-votes
- stored records in `data/design_evaluations.json`

## Verification order

1. `python3 -m py_compile backend/main.py`
2. `node --check` for inline frontend/admin scripts
3. restart backend on port `8090`
4. `curl /health`
5. `curl /workflow/templates?feature=design`
6. `curl /design/evaluate`
7. confirm `design_total` / `design_approved` in `/admin/metrics`

## Notes

- Keep the design brief focused on brand kit, poster, social story, logo concept, product photo, mockup, catalog, and landing hero.
- Use the live health check after restart; a short-lived uvicorn exit is not proof of failure if another process already serves `8090`.
