# Checkout table / form visual tuning

Use this when a user gives a screenshot/reference image and asks to make a static checkout page look closer to it.

## Workflow
1. Inspect the actual source HTML/CSS that renders the checkout, not only the built output.
2. Use vision analysis on the screenshot to identify the form structure first:
   - section order
   - single-column vs two-column blocks
   - borders/radius
   - spacing rhythm
   - button hierarchy
3. Apply the smallest source edits needed to match the visual rhythm:
   - adjust card padding and margin
   - narrow/widen border opacity and radius
   - tune input padding and line height
   - keep the same field order unless the screenshot clearly differs
4. If the page is static HTML served from `web/public/`, keep the source of truth there and sync any mirrors/build outputs only after the source is correct.
5. Rebuild, deploy, then verify the live page with HTTP or browser DOM/screenshot checks.

## Common pitfalls
- Changing copy or field order when the request only asks for spacing/border tuning.
- Verifying only with `grep` instead of checking the rendered live page.
- Forgetting to sync mirrored copies when the checkout page is maintained in multiple locations.
- Over-rounding cards and inputs: many dark checkout references use flatter 4–8px corners, thin borders, and generous but not oversized padding.
