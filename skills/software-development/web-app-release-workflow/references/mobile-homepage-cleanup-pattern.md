# Mobile Homepage Cleanup Pattern

Use this pattern when a user says the mobile site looks "berantakan", crowded, duplicated, or hard to read.

## Symptoms seen in this session
- Repeated headline/hero copy in the same viewport.
- Duplicate login/CTA blocks shown back-to-back.
- Large marquee/banner plus large hero text causing the page to feel stacked and noisy.
- Too much text competing with the menu strip on narrow screens.

## Fix strategy
1. Keep one primary hero statement only.
2. Remove redundant duplicate titles and repeated CTA blocks.
3. Collapse the intro into a short one-line helper plus 2–3 compact CTAs.
4. Reduce marquee prominence: smaller height, smaller font, softer border.
5. Preserve the existing menu/navigation structure; clean the wrapper content first.
6. Prefer source template edits in the PHP source tree, not build artifacts.

## Good mobile pattern
- 1 short intro line
- 1 compact CTA row
- 1 menu area
- no repeated headline block above the menu

## Verification
- Read the rendered mobile source file and confirm only one hero/title block remains.
- Search the file for duplicate CTA blocks before deploying.
- Prefer a quick content grep over visual guessing when the page is text-heavy.
