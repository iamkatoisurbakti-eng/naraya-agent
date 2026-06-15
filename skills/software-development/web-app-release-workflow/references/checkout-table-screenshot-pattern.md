# Checkout/table screenshot matching pattern

Use this when a user points to a screenshot of a checkout or form layout and asks you to make the live page look like it.

## Workflow
1. Inspect the screenshot with vision first and extract the structure, not just the styling.
2. Map the visible hierarchy into concrete source sections:
   - section order
   - field order
   - column splits vs full-width rows
   - button placement
   - summary/sidebar ordering
3. Edit the source HTML/CSS/React component, not the build output.
4. Keep the production flow intact; preserve validation and submission wiring unless the user explicitly wants a behavior change.
5. After the source patch, run build + deploy, then verify the live URL directly.

## Common layout pattern from checkout screenshots
- One prominent contact section and one address section are easier to match than a single dense form.
- Use a two-column split only where the screenshot clearly shows it; otherwise keep address fields full width.
- Country selectors often need to look like normal inputs/selects with a default value.
- If the screenshot shows a visible action button such as “Apply Address”, mirror it as a dedicated form action rather than burying the state update in unrelated controls.
- Keep the order of the summary panel aligned with the visible screenshot labels, even if the underlying payload keeps a different internal shape.

## Verification
- `npm run build:web`
- deploy script
- `curl` the live page and grep for the exact visible labels from the screenshot
- if needed, re-open the screenshot and compare field order/spacing before finalizing
