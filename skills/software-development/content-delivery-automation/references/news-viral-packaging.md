# News viral packaging: safe 10-card pipeline

Use this when turning current news into a flyer pack for social posting.

## Selection workflow
1. Collect a larger candidate set than needed (15-30 items) from current news sources.
2. Filter out taboo topics early: religion, politics, sexual content, and anything user flagged as off-limits.
3. Rank candidates by:
   - recentness / current-looking freshness
   - visual punch
   - clickability / shareability
   - how easily the story can be explained in 1 sentence
4. If multiple items are close, do a quick debate/vote across the shortlist and pick the strongest 10.

## Copy style for flyers
- Rewrite into short Indonesian Gen-Z/Jaksel tone when requested.
- Keep the visible title very short.
- Avoid repeated words inside the flyer text; vary wording across cards while keeping the template structure consistent.
- Do not let the copy sound like an article summary; make it feel like a social post hook.
- When the user asks for caption + hook + hashtag, treat them as separate outputs per card.

## Layout and rendering
- Keep one asset per story: 1 PNG per article/item.
- Use a consistent template system, but allow style variation between versions so the series does not feel copied verbatim.
- Keep text readable at feed size; prefer hierarchy over long paragraphs.
- If the hero/source image includes a visible watermark or publisher mark, first try a cleaner alternate image or crop. Do not let source branding remain visible in the final public-facing card.

## Output packaging
- Provide a manifest that maps each PNG to: title, hook, caption, hashtags, and source.
- Keep the manifest human-readable so it can be reused for Telegram or other channels.
- If the user wants the pack ready for posting, preserve one caption and one hashtag block per PNG.

## Verification checklist
- 10 items selected from the shortlist
- taboo-topic filter applied
- title/hook readable at thumbnail size
- no obvious copy repetition across cards
- 1 PNG per item saved
- caption + hashtag present for each item
- visual scan for clipping, watermark, and low-contrast text
