# Session: image fallback rotation and smaller assets

## Why this exists
A run produced a missing/invalid flyer image, so the news generator was hardened to always return a usable PNG instead of failing silently.

## Implemented fallback chain
In `scripts/genz-news.ts`, the image-data step now falls back in this order:
1. Primary Seedream/ARK image fetch
2. Rotated provider fallback via `scripts/prompt-to-images.ts --provider rotate`
   - uses `--providers ark,openai` by default when rotation is available
   - keeps `--watermark=false`
   - uses a larger generation size (`--size 2K`) for fallback robustness
3. Existing source image URL if present
4. SVG fallback so the final card still renders

## Invalid-image guard
The browser-side render step validates the loaded image before screenshotting the card:
- if the image fails to load, the template swaps to the fallback SVG
- if the image is tiny/invalid (`< 400x400`), it is treated as unusable and replaced

## Asset-size reduction for Seedance-friendly workflows
To make downstream video/image workflows easier to handle:
- `deviceScaleFactor` was reduced from `2` to `1` in the flyer renderer
- a smaller `1080x1350` derivative was generated from the larger PNG where needed

## Notes
- The user mentioned “byte1-15”, but the live implementation currently rotates providers via the provider list rather than a literal byte1..byte15 map.
- Keep the fallback visible in the manifest/logs so future runs can tell whether the primary provider or the rotation path was used.

## Verification
Recommended checks after changing the fallback logic:
- run one generation pass and confirm a PNG is produced even when the primary image path fails
- inspect the run folder for the final image file
- confirm the fallback provider path and browser-side validation still produce a valid screenshot
