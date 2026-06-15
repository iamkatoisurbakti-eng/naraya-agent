# Affiliate dashboard and video-studio model privacy

## What was implemented
- Added an auth-protected affiliate endpoint at `GET /api/payments/affiliate`.
- The endpoint returns one payload containing:
  - wallet summary
  - referral link
  - referral rows
  - earnings rows
  - withdrawal rows
  - aggregate stats
- Referral links use `?voucher=CODE` so the register modal can prefill the voucher field.
- The register modal also accepts `?ref=` as a fallback alias.
- Affiliate dashboard UI can be shown as a dedicated dashboard section and should stay customer-facing, not admin-only.

## Video Studio model privacy pattern
- If the user asks to remove the model chooser from Video Studio, hide only the manual selector in the Video Studio advanced area.
- Keep backend/model resolution automatic so video generation still uses the catalog/default model.
- Do not remove the model selector from other studios unless explicitly requested.
- Prefer a plain informational notice in the Video Studio advanced panel: the model is set automatically and there is no manual choice.

## Verification notes
- Build the web app after the UI change.
- If a new endpoint is added, add an API test that exercises it with a paid/referral flow.
- Use randomized emails in tests to avoid collisions with seeded/demo users or prior local runs.
