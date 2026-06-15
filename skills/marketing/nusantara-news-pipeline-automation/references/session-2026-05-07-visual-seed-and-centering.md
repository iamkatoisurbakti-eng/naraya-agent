# Session 2026-05-07 — Visual seed consistency and center-safe framing

Context: user requested consistent seeds and centered image/video framing so subjects are not cut off, then clarified that videos must also keep the action visible and uncropped.

Production pattern implemented in `/root/nusantara-ai-saas`:

- Env defaults:
  - `NEWS_VISUAL_SEED=24857`
  - `NEWS_VISUAL_CENTERING_GUARD=1`
- Deterministic per-story seed:
  - `news-pipeline.ts` derives a stable numeric seed from base seed + title + article/file/id.
  - Pass the same story seed to `prompt-to-images.ts` and `images-to-video.ts`.
  - Video scenes use `baseSeed + sceneIndex` for scene variation while keeping a consistent look.
- Prompt guard:
  - Image prompt includes a strict center-safe framing guard: main action in safe middle area, medium-wide shot, 10–15% margin, no cropped faces/heads/hands/bodies/vehicles/buildings/key evidence.
  - Video prompt repeats the same rule and asks for stable camera, clear central focus, and visible full context.
- Template guard:
  - `templates/nusantara_instagram_4x5.html` and `templates/nusantara_shorts_9x16.html` use `object-fit: contain` and `object-position: center center` for generated visual assets.
  - Add a blurred background fill layer so contain framing does not look empty/letterboxed.
- New template defaults:
  - Instagram: `/root/nusantara-ai-saas/templates/nusantara_instagram_4x5.html`
  - Shorts: `/root/nusantara-ai-saas/templates/nusantara_shorts_9x16.html`

Verification recipe:

```bash
cd /root/nusantara-ai-saas
npm run build:server
bash -n scripts/run-youtube-hourly-queue.sh
bash -n scripts/youtube-scheduled-upload.sh
npx tsx scripts/prompt-to-images.ts --dry-run --provider ark --prompt "uji adegan berita warga di lokasi" --output /tmp/test.png --seed 24857 --watermark=false > /tmp/center-image-dryrun.json
npx tsx scripts/images-to-video.ts --dry-run --prompt "uji video adegan berita warga di lokasi" --image-url https://example.com/test.png --seed 24857 --ratio 9:16 --output /tmp/test.mp4 > /tmp/center-video-dryrun.json
```

Check the dry-run JSON for:

- image payload has `seed: 24857`
- image prompt contains `safe middle area` / `No cropped heads`
- first video scene payload has `seed: 24858`
- video prompt contains `subjek/aksi utama tetap di tengah frame`

Pitfall: do not rely only on prompt wording. If the HTML overlay uses `object-fit: cover`, generated image/video can still be cropped by the template. Keep both prompt guard and CSS `contain + center center` in place.