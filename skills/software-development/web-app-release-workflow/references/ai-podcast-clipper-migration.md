# AI Podcast Clipper migration notes

Use this pattern when swapping the Nusantara AI Clipper backend from the old engine to AI Podcast Clipper while keeping the existing job contract stable.

## What changed in this session
- The visible engine name in the dashboard moved to AI Podcast Clipper.
- The backend kept the existing job shape (`youtubeUrl`, `clipGoal`, `targetDuration`, `outputFormat`, subtitle flags), so the dashboard contract did not need a redesign.
- The upstream engine was vendored into the repo and executed through a dedicated Python worker script.
- Docker runtime needed Python, ffmpeg, yt-dlp, ffmpeg-python, pysrt, and python-dotenv.

## Runtime notes
- Treat the upstream project as a Python dependency source, not a Node package.
- Keep the worker isolated so the Node backend only owns orchestration and job state.
- If the download step fails with YouTube bot/login text, add cookies-file support and a clear user-facing error instead of exposing the raw yt-dlp stack trace.
- A persistent default like `/app/data/youtube-cookies.txt` makes runtime support easier to document and verify.

## Verification
- Compile the worker script before shipping it.
- Run `npm run build` and `npm run test:api` after route/UI changes.
- Smoke test the public host after deploy; if YouTube blocks the sample video, verify the translated error path still reaches the user.

## Pitfalls
- Do not rename the job API just because the engine changed.
- Do not leave the dashboard on the old engine brand string after the backend has switched.
- Do not ask the user to paste cookies into chat; use file/env wiring only.
