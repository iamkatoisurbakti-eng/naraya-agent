# Gen-Z news pack session notes (2026-05-06)

This session produced a reusable pattern for viral news cards delivered to Telegram.

## Source and selection
- Source feed used successfully: `berita-indo-api-next`.
- Good candidates were filtered to exclude religion, politics, and sexual content.
- Shortlist ranking favored freshness + shareability + visual punch.
- When the user asked to “debat/voting” the top candidates, the practical pattern was: rank top items first, then choose among the close contenders before rendering.

## Rendering
- Working template: `/root/bot_template.html`.
- The cleaner look came from removing the left purple sidebar/accent bar and hiding the under-title description block.
- The visible headline should stay short; the under-title description should not appear in the final flyer when the user asks for a cleaner layout.
- BytePlus/ARK Seedream image generation worked with `watermark: false`.
- The final deliverable should be PNG; if the provider returns JPEG, download and transcode before upload.

## Caption format that worked
- Use distinct fields in the caption:
  - `Hook: ...`
  - `Viral momentum: ...`
  - CTA line
  - hashtags
- Keep each hook varied so the opener does not repeat across the 10-card pack.
- Keep the summary/momentum short enough that Telegram caption limits are not hit.

## Telegram delivery
- Delivery succeeded with `sendDocument` so the PNG stayed exact.
- Files were sent one-by-one.
- Keep bot tokens and chat IDs out of chat output; only verify them through env presence.

## Useful output paths
- Batch run directory example: `/root/nusantara-ai-saas/data/genz-news/2026-05-06T15-10-05-068Z/`
- Manifest example: `/root/nusantara-ai-saas/data/genz-news/2026-05-06T15-10-05-068Z/manifest.md`
