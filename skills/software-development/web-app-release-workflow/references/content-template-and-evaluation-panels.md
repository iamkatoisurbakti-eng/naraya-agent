# Content Template and Evaluation Panels

## Session pattern
- Add customer-facing dashboard sections as first-class panels, not hidden subpages.
- For this session, the app got two new productivity surfaces:
  - `Template`
  - `Evaluasi`

## Template panel
Purpose:
- help users create consistent professional content for:
  - produk
  - jasa
  - tempat
  - bisnis

Implementation notes:
- Use a reusable template panel with clear headings, brief positioning copy, and prompt text the user can copy.
- Keep the HTML template public under `web/public/templates/` so it is easy to open and reuse.
- Keep the visual language professional, clean, and reusable across brands.

## Evaluation panel
Purpose:
- let users upload reference content and ask an agent to review quality and growth direction.

Implementation notes:
- Accept uploaded references from the user.
- Ask for:
  - brand name
  - content type
  - audience
  - objective
  - notes
- Have the agent return:
  - summary
  - strengths
  - improvements
  - 7-day next steps
  - score

## Dashboard integration pattern
- Add sidebar items and quick cards for the new surfaces.
- Extend the active section union type carefully so navigation stays type-safe.
- Keep the new panels alongside ChatBox, API Scraper, and other app tools.

## Verification
- Run a production web build after wiring the new panels.
- Confirm the new buttons exist in the dashboard.
- Confirm the HTML template is reachable directly from `/templates/...`.
- Keep the experience end-to-end inside the app so users do not have to leave Nusantara AI to use the template or evaluation flow.
