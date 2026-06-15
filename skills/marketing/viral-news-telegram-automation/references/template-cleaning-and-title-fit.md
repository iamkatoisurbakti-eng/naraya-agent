# Template cleaning and title-fit notes

This session found a better baseline for the viral-news flyer template and headline handling.

## Clean template changes that worked
- Background: slightly darker radial gradient for a cleaner premium feel.
- Card: increase height from 450px to 480px and round corners a bit more.
- Image slot: reduce image height slightly to give the lower panel more breathing room.
- Badge/category: make badge more subtle and reduce visual noise.
- Lower panel: increase height so the title has enough vertical space.
- Title: reduce font-size a little and enable wrapping safeguards.

## Headline fit fix that mattered
The card headline was initially too aggressively shortened, which caused awkward ellipses like `Bisa Beru...`.

Fix:
- Let `buildCardHeadline()` keep more words before truncating.
- Prefer 8 words and only ellipsize past a higher character threshold.
- Keep `word-break: break-word`, `overflow-wrap:anywhere`, and balanced wrapping in the template.

## Verification recipe
1. Run a single-item dry run:
   - `npm run gen:viral-news -- --count 1 --dry-run`
2. Check the output PNG with a vision pass:
   - confirm no left purple sidebar
   - confirm no extra summary line under the title
   - confirm the headline is fully readable or at least not awkwardly clipped
3. If the title clips, adjust in this order:
   - lower the title font size slightly
   - increase card height or lower-panel height
   - relax `buildCardHeadline()` truncation

## Notes
- The generated manifest is useful for quick caption checks, but the PNG itself is the real source of truth for layout.
- Keep the template clean first; do not compensate for a bad template by over-truncating headlines.