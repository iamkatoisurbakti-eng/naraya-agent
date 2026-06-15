# Gen-Z viral news pack + BytePlus ARK pipeline notes

Session-proven pattern for current-news flyer packs:

## Source + selection
- Source used in session: `berita-indo-api-next` news routes.
- Pull a larger shortlist than needed first, then prune to the final 10.
- Hard-filter taboo topics early: religion, politics, sexual content.
- Rank remaining items by freshness, visual punch, and shareability.
- If top candidates are close, do a quick debate/vote before locking the final pack.

## Copy rules
- Rewrite into short Indonesian Gen-Z / Jaksel style when requested.
- Keep each card's lead phrase distinct; do not repeat the same hook words across the whole pack.
- Keep visible card text short so it fits cleanly in a feed-sized flyer.
- Output one caption + one hashtag block per PNG.
- If the user asks for a clean social asset, do not print source labels on the flyer.

## Rendering + image generation
- Working template in this session: `/root/bot_template.html`.
- BytePlus/ARK image generation worked with Seedream-style calls and `watermark: false`.
- Use `response_format: "url"` and download the returned image locally before reuse.
- Some responses may return JPEG URLs; transcode to PNG if the downstream delivery expects PNG.
- For deterministic local steps, use `python3` if `python` is missing.
- If Pillow install is needed in this environment, `python3 -m pip install --user --break-system-packages pillow` was the successful path.

## Delivery + packaging
- Emit 1 PNG per item.
- Save a human-readable `manifest.md` that maps each image to title/hook/caption/hashtags.
- Dry-run a single item first, then scale to the full batch once the layout and copy look right.
- For long-running batch renders, add timeouts to fetch/generation/download steps so the process does not hang forever.

## Pitfalls observed
- Browser/template mismatches can waste time; verify the actual template root before wiring render logic.
- Watermark removal should happen at generation time when possible; do not rely on post-processing alone.
- Source content can be current but still too close to off-limits topics; the final human review still matters.
- Batch renders may succeed unevenly; inspect the last few items for clipping or truncated subtitles.
