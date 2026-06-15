# Single-flyer render and verification notes

Use this when the request is simply “buat 1 flyer” or “coba buat 1 flyer”.

## Recommended flow
1. Run the news generator for a single item:
   - `npm run gen:viral-news -- --count 1`
2. Inspect the newest `data/genz-news/<timestamp>/` folder.
3. Prefer the rendered PNG produced by the Instagram template output, not the raw source image.
4. Verify the file exists and is a real image:
   - `file <path-to-png>`
   - optionally check dimensions with ImageMagick or another local image tool.

## Important pitfall
- The generator may render the flyer successfully and still exit non-zero afterward if Telegram env vars are missing.
- If that happens, do not assume the render failed: check the PNG path mentioned in the log and validate the file directly.
- For a clean end-to-end run, provide the required Telegram env vars or use a dry-run/testing path.

## Visual direction for 4:5 flyers
- Keep the hero image as full-bleed as possible inside the 4:5 frame.
- Use centered composition and minimal inner padding so the image feels closer to edge-to-edge.
- Keep the title panel and footer readable, but avoid wasting the hero area with large empty margins.
