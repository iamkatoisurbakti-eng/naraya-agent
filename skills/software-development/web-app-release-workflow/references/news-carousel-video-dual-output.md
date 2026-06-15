# News carousel + short video dual-output workflow

Use this when each generated news item must produce two final deliverables:
1. Instagram carousel image in 5:4
2. YouTube Short / vertical video using the generated image as the reference frame

## Required order
1. Generate the news item and its caption first.
2. Generate the Instagram image first via `prompt-to-images`.
   - Target format: 5:4
   - The image must be clearly about the news title/topic.
   - Do not show source labels in the visible artwork.
3. Feed the resulting image URL/path into `images-to-video` as the reference image.
4. Force the short video to stay news-driven and long enough for Shorts.
   - Minimum duration: 30 seconds
   - Headline/title must remain visually explicit in the final video
5. Store both captions separately if the pipeline reports them:
   - `instagramCaption`
   - `youtubeCaption`

## Caption requirements
- Hook viral must be explicit.
- CTA must be present.
- Hashtags must stay consistent with the news brand.
- Keep the public branding as `Nusantara-AI News`.
- Do not render visible source/sourceLabel text in the public output.

## Practical implementation notes
- The image generation step should return an output URL/path that can be passed straight into the video step.
- When the video step supports `image_url` / `reference_image`, prefer that over copying a stale local asset.
- Default or coerced video duration should be at least 30 seconds for this workflow.
- For vertical Shorts, use 9:16 and keep the final raster at least 720x1280 (or higher) so the output passes minimum-resolution checks.
- In reports/manifests, preserve both the image artifact path and the reference image URL so the provenance is obvious.

## Verification
- Confirm the news pipeline produces both outputs for one item.
- Confirm the image is 5:4.
- Confirm the video references the generated image.
- Confirm the caption output contains hook viral + CTA.
- Confirm public-facing pages still hide source labels.
