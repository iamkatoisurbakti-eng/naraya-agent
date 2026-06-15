# Clipper / yt-dlp subtitle 429 pitfall

Observed failure:
- AI clipper job reached `download`/`subtitle-package` and then failed with `yt_dlp.utils.DownloadError`
- Raw cause was `HTTP Error 429: Too Many Requests` while downloading YouTube subtitles
- The failure came from subtitle retrieval, not from the actual clip render

What fixed it:
- Treat subtitle download as optional
- Catch subtitle download exceptions in the worker and continue rendering the clip
- Keep the main video download/render path separate from subtitle fetching

Useful reproduction pattern:
1. Register/login a test user
2. Create a clipper job for a YouTube URL
3. Poll `/api/clipper/jobs/:jobId`
4. If status fails and the stack mentions `_write_subtitles`, inspect subtitle config before changing clipping logic

Verification:
- Build succeeds
- API tests pass
- Live smoke test completes with `clip.mp4` even when subtitle fetch is rate-limited

Related symptoms to look for:
- `Unable to download video subtitles`
- `HTTP Error 429`
- `_write_subtitles`
- `subtitle-package` stage failing while `clip-render` is still fine
