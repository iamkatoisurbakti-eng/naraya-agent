# Feed Design Rendering for News Cards

Use this when the user wants a *single Instagram feed post* (4:5) rather than the full image+video Telegram pack.

## Goal
- Produce a clean, ready-to-post 4:5 feed image.
- Keep the layout editorial and bold.
- Avoid visible source labels or technical footer text in the final asset.

## Working recipe
1. Build the card as an SVG or HTML composition with a 1080x1350 canvas.
2. Keep the structure simple:
   - small top pill / section label
   - large ALL-CAPS headline
   - short dek or 2–3 bullets
   - CTA question at the bottom
3. Use a dark black base with one accent color (red in this user’s case).
4. If you must use a source photo:
   - crop it so embedded source overlays/watermarks are removed
   - place it as a cut-out or framed hero image
5. Render deterministically:
   - SVG -> PNG with `ffmpeg -i card.svg -frames:v 1 -update 1 out.png`
   - if browser preview is flaky or times out, prefer the ffmpeg render path over repeatedly retrying browser navigation
6. Verify the output visually before sending:
   - headline readable at small size
   - no clipped CTA/footer text
   - no source/watermark labels visible
   - safe margins remain inside the Instagram crop area

## Notes from session
- A direct browser preview of a local feed HTML can time out; using an SVG composition plus ffmpeg rendering is more reliable.
- Embedded source labels from provider images can survive unless the image is cropped or replaced.
- A final vision check is useful to confirm that source branding is gone and the CTA is not too close to the edge.
