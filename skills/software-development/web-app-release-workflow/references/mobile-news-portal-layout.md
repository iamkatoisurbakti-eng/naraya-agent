# Mobile News Portal Layout Notes

Use this pattern when turning `news.*` into a portal/majalah-style experience that must stay usable on phones.

## Mobile layout goals
- One dominant hero story first.
- Keep the masthead visible but compact.
- Make category chips horizontally scrollable; avoid wrapping chip storms.
- Keep one clear CTA row; stack buttons vertically on narrow screens.
- Reduce the number of visible controls above the fold.

## Practical mobile fixes that helped
- Add explicit line breaks to long portal headlines so they do not clip on 390px screens.
- Limit hero copy width with `max-w-*` and a tighter line-height.
- Hide or soften heavy media on phones if it hurts readability.
- Keep side-rail blocks compact: breaking line, editor’s pick, and status cards should be short and scannable.
- Use `overflow-x: hidden`, `touch-action: manipulation`, and `scroll-padding-top` in global styles.

## Verification
- Rebuild the frontend.
- Deploy.
- Capture a real mobile viewport screenshot (for example Chromium headless at 390x844).
- Check for:
  - clipped headlines
  - cramped chips
  - horizontal overflow
  - too many controls above the fold
  - CTA buttons too small to tap
