# Nusantara-AI News image-first pipeline

## What changed in this session
- Public brand: `NUSANTARA-AI NEWS`.
- Public output must not show source labels.
- Each news item now produces 2 deliverables:
  1. Instagram image, 5:4 aspect ratio.
  2. YouTube Shorts video, minimum 30 seconds.
- The image must be generated first, then passed into video generation as the reference image.
- The pipeline now records both captions separately (`instagramCaption` and `youtubeCaption`) even when the copy is intentionally similar.

## Automation pattern
1. Generate the news item / article record.
2. Build the Instagram prompt and render the 5:4 image with `prompt-to-images`.
3. Reuse the resulting image URL/path as `reference_image` for `images-to-video`.
4. Post-process the video to keep the headline visible.
5. Upload / deliver the final files.

## Provider switch
- `prompt-to-images.ts` supports `--provider ark` and `--provider openai`.
- OpenAI mode uses `OPENAI_API_KEY` and defaults to `gpt-image-2`.
- News pipeline can select the provider via `NEWS_IMAGE_PROVIDER` / `IMAGE_PROVIDER`.
- Keep secrets only in env vars; never hardcode or echo them.

## Subdomain / host routing
- `news.nusantara-ai.online` should run in news-only mode.
- Root on the news host redirects to `/news`.
- `CLIENT_ORIGIN` should include both the main domain and the news subdomain, comma-separated.

## Pitfalls
- Do not copy or reuse source labels into the rendered public asset.
- Do not generate the video first; the image should be the reference input.
- Keep the video short but not too short: enforce a 30s floor for Shorts.
- If the user asks for a news-only website, make the host-based route separation explicit instead of burying it behind the main dashboard shell.
- When switching image providers, verify dry-run output first so the payload shape is correct before any real API call.
