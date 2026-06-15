# ASPRI Feature-Family Verification

Use this reference when working on `/root/nusantara-agent/aspri-nusantara-app` or a similar FastAPI + static HTML app that exposes multiple feature workflows.

## Stable pattern

- Backend runs on port `8090`.
- If a global `uvicorn` is missing, use the repo virtualenv launcher: `./.venv/bin/uvicorn`.
- Edit source files, not build output.
- Verify backend syntax, frontend JS syntax, live HTTP endpoints, and any persistence files touched by the change.

## Feature-specific workflow map

- `video` and `content` use shared workflow plumbing, but the templates/payloads differ.
- `bantu` covers WhatsApp/Instagram automation and should include autoreply, escalation, and audit-style checks.
- `belajar` uses 24h nonstop debate/voting/scoring and only auto-adds approved material when `score > 80`.
- `bisnis` uses multi-agent debate plus backtesting/loop evaluation; apply changes only when approved and `score > 80`.
- `keuangan` uses debate/audit/validation; apply changes only when approved and `score > 80`.
- `design` covers brand kit, poster, social story, logo concept, landing hero, and dedicated 24h multi-agent evaluation; verify `/workflow/templates?feature=design`, `/feature/design`, `/workflow/run`, `/design/evaluations`, and `/design/evaluate`.
- `hobby` covers sports meetups for padel, basket, tennis, running, badminton, golf, and other community sports; verify `/workflow/templates?feature=hobby` and `/feature/hobby`.
- `pos` covers kasir, invoice, struk, mark-paid, and revenue metrics; verify both creation and paid transitions.
## Endpoints worth verifying

- `/health`
- `/features`
- `/workflow/templates?feature=...`
- `/workflow/run`
- `/learning/materials`, `/learning/evaluate`
- `/business/evaluations`, `/business/evaluate`
- `/bantu/evaluations`, `/bantu/evaluate`
- `/keuangan/evaluations`, `/keuangan/evaluate`
- `/finance/evaluations`, `/finance/evaluate` (alias)
- `/modul/evaluations`, `/modul/evaluate`
- `/pos/invoices`, `/pos/invoices/{invoice_id}`, `/pos/invoices/{invoice_id}/mark-paid`
- `/feature/design`
- `/design/evaluations`
- `/design/evaluate`
- `/feature/hobby`
- `/admin/metrics`

## Verification order

1. `python3 -m py_compile backend/main.py`
2. `node --check` for inline `<script>` blocks in `frontend/index.html` and `admin/index.html`
3. Restart the backend after edits
4. `curl` the health endpoint
5. `curl` the feature-specific endpoint(s)
6. Confirm the touched `data/*.json` file changed as expected
7. Re-check admin metrics for totals and approval counts
8. For ASPRI/Nusantara apps, verify `design` and `pos` in `/features` and smoke-test the matching endpoints before closing
9. If a new `uvicorn` start exits with `-15` or fails to bind `8090`, confirm whether a live process is already serving `/health` before restarting again

## Threshold and payload pitfalls

- Borderline payloads may land exactly on `80` and must not be treated as approved if the rule is `> 80`.
- Stronger successful submissions in this app usually include explicit details for:
  - risk and validation for bisnis/keuangan
  - backtesting for modul/bisnis
  - clear automation channels for bantu
  - concrete lesson structure and examples for belajar
- If verification only tests a weak example, add a stronger payload before concluding the threshold logic is correct.

## Persistence files observed in this session

- `data/learning_materials.json`
- `data/business_evaluations.json`
- `data/bantu_features.json`
- `data/finance_evaluations.json`
- `data/module_evaluations.json`
