# 5:4 video export with `genz.html`

Current working pattern discovered in session:

- Video title overlay script: `/root/nusantara-ai-saas/scripts/genz-news-video-title.ts`
- NPM command: `npm run gen:viral-news:video-titles`
- Template argument: `--template /root/genz.html`
- Aspect argument for 5:4 export: `--aspect 5:4`
- Output suffix: `-5x4.mp4`

Verification:
- Use `ffprobe` on a sample output to confirm `width=1080` and `height=864`.
- The generated `video-title-manifest.json` should point to the 5x4 files.

Pitfall:
- Do not assume the script uses 5:4 by default; pass `--aspect 5:4` explicitly when the user requests it.
- Keep the `drawtext` filter minimal; avoid injecting template notes into ffmpeg filters.
