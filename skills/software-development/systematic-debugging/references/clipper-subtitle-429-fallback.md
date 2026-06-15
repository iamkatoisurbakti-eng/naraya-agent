# Clipper subtitle 429 fallback

Context:
- In the AI Podcast Clipper worker, subtitle downloads via yt-dlp can fail with HTTP 429 or other temporary YouTube limits.
- If subtitle download is treated as fatal, the whole clip job fails even when the main video render succeeded.

Observed failure pattern:
- Job starts normally.
- Environment check passes.
- yt-dlp fails while writing/downloading subtitles.
- Worker exits with a subtitle-related error and leaves the job in failed state.

Recommended behavior:
1. Keep the main video download/render path independent from subtitle fetch.
2. Treat subtitle download as optional when the user asked for subtitles.
3. Wrap subtitle fetch in try/except and continue with raw clip output if it fails.
4. Only fail the job if the primary video download/render fails.
5. If subtitles are required for a specific deployment, surface a clear error that points to cookies/rate-limit issues; otherwise, degrade gracefully.

Useful signal:
- yt_dlp.utils.DownloadError
- HTTP Error 429: Too Many Requests
- subtitle step stalled while clip render would otherwise succeed
