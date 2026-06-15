# YouTube Clipper feature integration notes

Use when adding a productized YouTube clipper feature to the Nusantara AI SaaS style app.

## Pattern used
- Treat `https://github.com/VadlapatiKarthik/autoclipper` as the actual clipper engine for the Nusantara AI Clipper feature, not merely documentation/reference.
- Productize the feature in two layers:
  1. Auth-protected backend job endpoint that validates YouTube URLs and dispatches the AutoClipper workflow/worker.
  2. Dashboard UI form/card that creates the job and displays queued/running/completed stages/outputs from the worker.
- Good endpoint shape:
  - `POST /api/clipper/jobs`
  - Require `Authorization: Bearer <token>` via existing `requireAuth` middleware.
  - Accept `youtubeUrl`, `clipGoal`, `targetDuration`, `outputFormat`, `subtitles`, `burnSubtitles`.
  - Validate hosts: `youtube.com`, `www.youtube.com`, `m.youtube.com`, `youtu.be`.
  - Extract video ID from `?v=` or youtu.be path.
  - Return `201` with `product: 'NUSANTARA AI - CLIPPER'`, `jobId`, `source`, `request`, queued `stages`, expected `outputs`, and `engine` reference metadata.

## UI pattern
- Add a dashboard section titled `NUSANTARA AI - CLIPPER`.
- Include fields for YouTube URL, clip goal, target duration, output format, bilingual subtitles, and burn-subtitle option.
- Show pipeline stages after submit, not just a toast, so the user sees the feature exists and the workflow is concrete.
- Add Quick Create/menu entry with YouTube/scissors icon; `react-icons/fa6` includes `FaYoutube` and `FaScissors`.
- If the user asks to show Clipper on the front of Nusantara AI Studio, update the landing page too: add a navbar `Clipper` anchor, add a `NUSANTARA AI - CLIPPER` studio card near Images/Video/Music/Chat, and have `BUKA AI CLIPPER` open auth/dashboard rather than an inert button.
- After a landing-page addition in a Vite SPA, verify the compiled JS bundle contains the new text/anchor; the root HTML alone will not contain React-rendered content.

## Engine integration details
The user corrected that `https://github.com/VadlapatiKarthik/autoclipper` is the actual engine to use, not a loose reference.
- Vendor or install the repo into the app runtime, e.g. `vendor/autoclipper`, and dispatch its scripts from the backend worker.
- Runtime Docker image must include `python3`, `pip`, `ffmpeg`, and Python deps used by the engine such as `yt-dlp`, `pysrt`, `python-dotenv`, and `ffmpeg-python`.
- Verify runtime inside the container before claiming real rendering is live:
  - `python3 -c "import yt_dlp,pysrt"`
  - `ffmpeg -filters | grep subtitles`
  - `test -f vendor/autoclipper/backend/app/services/clipper.py`
- Backend should persist `clipper_jobs` with job id/user id/source/request/status/stages/outputs/error and expose:
  - `POST /api/clipper/jobs` to enqueue and start the skill worker
  - `GET /api/clipper/jobs/:jobId` to poll progress
- Serve finished artifacts from a controlled static prefix such as `/clipper-output/<jobId>/<file>` while storing files under a data volume.
- Worker stage mapping:
  - environment check -> validate Python deps, yt-dlp, FFmpeg/libass subtitle support
  - download -> run `scripts/download_video.py`
  - semantic chapter / clip render / subtitle package -> run skill scripts or mark pending until implemented
  - export -> expose generated MP4/SRT/summary links
- Output package should include MP4 clip, subtitle file when enabled, and a content summary markdown.

## Verification checklist
- Add/extend API test for authenticated `/api/clipper/jobs` returning `201` and correct video ID/stages.
- Add/extend e2e test to submit the dashboard form and assert job ID/output labels appear.
- For real engine integration, also verify the production container runtime:
  - Python imports for skill dependencies
  - FFmpeg subtitle filter availability
  - vendored/installed skill scripts exist in the image
- Run:
  - `npm run typecheck`
  - `npm run test:api`
  - `npm run build:web`
  - `npm run test:e2e`
  - `npm run test:unit`
  - `npm run test:live`
- Deploy via `bash scripts/deploy.sh`, then verify live health and Docker Compose healthy state.

## Pitfalls
- The production Docker image may not include yt-dlp/FFmpeg, so do not claim real video rendering is active unless those binaries and job workers are installed and verified in runtime.
- Do not embed or echo API keys/JWTs from live-test output.
- Keep source edits in `src/...` and `web/src/...`; do not patch `dist` directly.
- Patch tool lint output may be noisy if it runs single-file TypeScript without project config; rely on `npm run typecheck` for authoritative verification.
