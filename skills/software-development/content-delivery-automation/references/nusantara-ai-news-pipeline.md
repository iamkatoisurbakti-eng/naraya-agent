# Nusantara-AI News Pipeline Notes

Use this note when building or changing the Nusantara-AI news automation flow.

## Session-proven flow
1. Generate news items from approved multi-source feeds.
2. Auto-write a matching internal article per generated story.
3. Render two deliverables per story:
   - one Instagram image in 5:4
   - one short video (news-first, headline always visible)
4. Upload short video to YouTube Shorts when OAuth env is present.
5. Send final artifacts to Telegram.
6. Emit a final pipeline report when all steps finish.

## Branding and visible-copy rules
- Public-facing brand: `NUSANTARA-AI NEWS`.
- Keep Jaksel/Gen-Z writing style, but make it KBBI-friendly.
- Never show source labels in public-facing news cards, videos, captions, or article listings.
- If a source is needed for internal ranking, keep it in metadata only.

## Asset rules
- Every news item should have:
  - a hooky caption
  - hook-style hashtags
  - an Instagram 5:4 image asset
  - a video asset whose headline is part of the visual
- Videos must visibly contain the news title/headline, not generic motion visuals.
- For Instagram image output, use 5:4 instead of the older generic image packaging.

## Automation helpers added in this session
- `npm run ark:prompt-to-images`
- `npm run ark:images-to-video`

Both helpers use Ark/BytePlus-style env config and support `--dry-run`.

## Subdomain note
- `news.nusantara-ai.online` is treated as the news-only host in the frontend router.
- The news subdomain should only expose article/news routes, not the dashboard shell.

## Pitfalls observed
- Do not leak real tokens from helper files or pasted curl examples.
- A dry-run can succeed while the downstream upload steps are still skipped; verify each stage separately.
- When a template or brand is renamed, update both the render layer and the public-facing article UI so they stay aligned.
- If a source label is still visible anywhere, treat it as a bug even if the internal metadata is correct.
