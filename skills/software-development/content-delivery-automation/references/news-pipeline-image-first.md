# Nusantara-AI News: Image-First, Two-Output Pipeline

Session note for the latest Nusantara-AI News automation shape.

## Required output per story
- 1 Instagram deliverable in 5:4
- 1 YouTube Shorts deliverable, minimum 30 seconds in full-run mode
- Each story should still retain article generation and final report output

## Required order
1. Generate the story/article metadata.
2. Generate the Instagram 5:4 image first with `prompt-to-images`.
3. Capture the resulting image URL/path as `referenceImageUrl`.
4. Generate the short video with `images-to-video` using the Instagram image as the reference image.
5. Burn the title/headline into the final MP4.
6. Publish/upload/send only after both deliverables exist.

## Caption convention
- Reuse the same story caption structure for both outputs, but keep the fields separate in manifests:
  - `instagramCaption`
  - `youtubeCaption`
- Required fields:
  - `Judul: ...`
  - `Hook viral: ...`
  - `Inti cerita: ...`
  - short CTA
  - hashtags that include `#HookViral`

## Reporting convention
Per-item report should keep:
- `image5x4Path`
- `referenceImageUrl`
- `instagramCaption`
- `youtubeCaption`
- `rawVideoPath`
- `shortVideoPath`
- `youtubeUrl`
- `telegramSent`

## Pitfalls
- Do not treat the news image as a copy of the video stage; the image must be generated first and then reused as the reference for video generation.
- If the reference image is missing, skip or fail only that item rather than collapsing the whole batch.
- Keep source labels out of public captions and assets.
