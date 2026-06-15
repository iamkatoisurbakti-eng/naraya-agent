# Checkout summary panel mirroring

Use this pattern when the user points at a screenshot and asks to make a checkout/summary panel look similar.

## What to extract from the screenshot
- Panel hierarchy: title, sections, line items, total, payment note, CTA.
- Alignment: left label / right amount, with amounts always right-aligned.
- Spacing: panel padding, section padding, divider thickness, row gaps.
- Shape: border radius, border opacity, card background, input/row density.
- Accent details: info dot, badge style, recurring/one-time grouping, emphasized total.

## Typical implementation steps
1. Use vision/screenshot analysis to identify the exact section structure and visual tokens.
2. Rework the source markup to match the hierarchy before tuning colors.
3. Split the summary into semantic blocks such as:
   - recurring payment
   - one-time charges
   - total
   - accepted payment method
   - CTA
4. Use a wrapper panel with subtle border and inner section dividers.
5. Keep line items as two-column flex rows; keep totals bold and slightly larger.
6. If an item needs explanation, use a tiny inline info dot instead of long helper text.
7. After replacing the markup, remove obsolete bindings/IDs from the old layout and update JS helpers so they no longer assume removed summary fields exist.
8. Rebuild, deploy, and verify the live page with curl/grep for the new summary text and classes.

## Common pitfalls
- Leaving stale IDs like `sumPackage`, `sumAmount`, or `summaryStatus` in helper code after the markup changed.
- Letting section spacing get too dense; the reference usually looks better with more vertical breathing room.
- Making the border too strong; the reference uses a thin, low-contrast outline.
- Adding too many visual separators; use one wrapper border and a few subtle section dividers.
