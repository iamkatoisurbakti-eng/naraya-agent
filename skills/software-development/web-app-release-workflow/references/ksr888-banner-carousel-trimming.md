# KSR888 banner carousel trimming

Use this note when a host-specific PHP page already merges banners from a DB table plus local fallback files, and the user wants to remove the first one or two slides.

Observed pattern:
- Desktop and mobile sliders build `$bannerItems` from `tb_banner ORDER BY id ASC`.
- Fallback files from `/banner/*` are appended afterward.
- The live carousel uses the finalized `$bannerItems` array for both indicators and slides.

Safe trimming approach:
1. Build the full banner list first.
2. Deduplicate / `array_values(...)` to normalize indexing.
3. Remove the unwanted leading slides with `array_slice($bannerItems, N)` before rendering.
4. Keep indicators and `.item.active` logic on the trimmed array so slide indexes stay aligned.

Useful verification:
- Fetch the live page HTML and confirm the expected number of banner `src` URLs.
- Probe the final banner image URLs directly with HTTP 200 checks.
- Rebuild and recreate the PHP web container if the change is served from the image, not the working tree.