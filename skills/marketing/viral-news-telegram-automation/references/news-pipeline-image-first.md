# News pipeline: image-first video flow

Observed update from the Nusantara-AI news automation session:

- Instagram output is generated first with `scripts/prompt-to-images.ts`.
- The resulting image URL is passed into `scripts/images-to-video.ts` as `--image-url`.
- Video prompt should explicitly reference the Instagram image as the visual anchor.
- This keeps the short video aligned with the 5:4 Instagram asset and the news headline.
- The pipeline report should record both:
  - `image5x4Path`
  - `referenceImageUrl`

Recommended stage order:
1. generate news items
2. generate Instagram 5:4 images with `prompt-to-images`
3. generate short video with `images-to-video` using the image output as reference
4. overlay title / publish / Telegram / report

Useful checks:
- Confirm `prompt-to-images` returns `outputUrl` before starting video.
- If `outputUrl` is missing, fail that item early instead of generating video from a null reference.
- Keep the Instagram prompt explicit about 5:4 composition and visible title legibility.
