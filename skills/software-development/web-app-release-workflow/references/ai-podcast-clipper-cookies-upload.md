# AI Podcast Clipper cookies upload pattern

When YouTube blocks yt-dlp with "Sign in to confirm you’re not a bot" or similar cookie/login errors, the repo can support a user-supplied Netscape cookie blob in the clipper job request.

Implementation pattern:
- Add an optional UI textarea for Netscape-format cookies in the clipper panel.
- Submit it as `cookiesText` alongside the normal clipper request fields.
- On the server, validate the text size, normalize trailing newline, and write it to a per-job file under the job output directory, for example `data/clipper-jobs/<jobId>/youtube-cookies.txt`.
- Pass the file path to the worker via env vars:
  - `YT_DLP_COOKIES_FILE`
  - `YOUTUBE_COOKIES_FILE`
- In the worker, resolve cookies in this order:
  1. `YT_DLP_COOKIES_FILE`
  2. `YOUTUBE_COOKIES_FILE`
  3. default runtime path such as `/app/data/youtube-cookies.txt`
- Route all yt-dlp calls through one helper so download, subtitle fetch, and metadata probes all share the same cookiefile/options.
- Keep the user-facing error simple: explain that YouTube blocked the server and cookies are needed, instead of surfacing the raw yt-dlp stack trace.

Verification:
- Run a public video smoke test without cookies to confirm the friendly block message.
- Run the same job with a minimal Netscape cookie file payload to confirm the clip completes.
- Rebuild and redeploy after both frontend and backend changes.
