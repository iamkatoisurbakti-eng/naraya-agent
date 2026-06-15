# News Flyer Workflow

Use this workflow when the user asks for a news flyer, poster, or article-card PNG.

## Goals
- One PNG per article
- Use a real news image from the article page when available
- Keep the title short and the summary Gen-Z style when requested
- Remove source text from the flyer if the user asked for no source
- Deliver each flyer separately to Telegram when requested

## Practical Steps
1. Collect 10 article URLs or article records.
2. Fetch the article page and extract:
   - title
   - summary/body snippet
   - primary image (`og:image` or equivalent)
3. Normalize the headline into a short poster title (1-3 words when the user wants terse titles).
4. Build a fixed flyer layout with:
   - top image area
   - bottom text panel
   - consistent spacing and typography
5. Render each flyer to a separate PNG file.
6. Verify at least one sample with visual inspection to confirm:
   - the image is present
   - the text is legible
   - the composition is not broken
7. If Telegram delivery is needed, send one PNG per message/file.

## Notes
- If the source page has no usable image, use the best available in-article visual rather than a pure text-only design.
- Avoid cramming multiple stories into one flyer unless the user explicitly requests a collage.
- If the user dislikes source text on the flyer, remove it from the composition entirely rather than shrinking it.
