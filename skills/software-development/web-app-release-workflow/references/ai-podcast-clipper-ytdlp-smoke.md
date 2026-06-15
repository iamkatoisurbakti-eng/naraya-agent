# AI Podcast Clipper yt-dlp smoke and cookies notes

Session takeaway:
- For headless/public YouTube clipping, the worker should not depend on a brittle direct yt-dlp call path.
- Use a helper that centralizes yt-dlp options, including a cookiefile resolver and a `skip_download` variant for initial metadata probes.
- Default cookie path used in this repo: `/app/data/youtube-cookies.txt`.
- Allow cookie path overrides through env (`YT_DLP_COOKIES_FILE` / `YOUTUBE_COOKIES_FILE`) so Docker and local runs can share the same code path.
- If yt-dlp returns `Sign in to confirm you’re not a bot`, treat it as a YouTube headless-block issue, not a generic worker crash.
- Translate the raw error into a user-facing message that tells the user to provide Netscape cookies and retry.
- Verify fixes with two kinds of smoke tests:
  1. a known public video that should complete
  2. a video that is likely to trigger bot/cookie protection, to confirm the job fails cleanly and reports a readable error
- The useful success criterion is not “never fails”; it is “completes when possible and fails with an actionable message when blocked.”
