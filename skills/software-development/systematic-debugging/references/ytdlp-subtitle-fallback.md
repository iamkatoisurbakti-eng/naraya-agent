# yt-dlp subtitle failures in clipper jobs

Observed issue:
- Clipper jobs could reach `environment-check` and stall/fail when subtitle download was treated as mandatory.
- yt-dlp could raise `DownloadError: Unable to download video subtitles ... HTTP Error 429` even when the source video itself was otherwise accessible.

Root cause pattern:
- Subtitle fetching is a separate YouTube request path from the main video download.
- When subtitle retrieval is required for the whole job, a rate-limit or anti-bot response on subtitles aborts the entire clip workflow.

Fix pattern:
1. Keep source video download and clip render independent of subtitle retrieval.
2. Make subtitle download best-effort: wrap it in `try/except` and continue if it fails.
3. Preserve the clip output and summary even when subtitles are missing.
4. Only fail the job if the core video download/render path fails.

Verification:
- Submit a clipper job with subtitles enabled.
- Confirm the job can still complete if subtitle fetch returns 429.
- Check that completed jobs still emit `clip.mp4` and `summary.md`.
- If subtitles fail, ensure the failure is isolated to subtitle artifacts, not the whole job.
