# AutoClipper integration notes

Use when updating the Nusantara AI Clipper feature to use VadlapatiKarthik/autoclipper as the execution engine.

## What changed in this session
- Source engine reference now points to `https://github.com/VadlapatiKarthik/autoclipper`.
- A dedicated Python worker was added at `scripts/autoclipper-worker.py` so the Node backend can spawn AutoClipper in an isolated runtime.
- Docker runtime needs Python + ffmpeg support plus the Python dependency set used by AutoClipper.

## Repo shape worth remembering
From the upstream repo, the useful files were:
- `backend/app/services/clipper.py`
- `backend/app/services/subtitle.py`
- `backend/app/services/youtube.py`
- `backend/app/requirements.txt`

The implementation pattern that translated well into Nusantara AI SaaS was:
- keep the existing auth-protected job model in the backend
- let the worker accept YouTube URL + clip parameters
- return stage/output metadata to the dashboard instead of hiding work behind a toast

## Runtime and build notes
- Runtime Python deps included `yt-dlp`, `pysrt`, `python-dotenv`, and `ffmpeg-python`.
- Verify the worker script before integrating: `python3 -m py_compile scripts/autoclipper-worker.py`.
- Verify app integration with `npm run build` and `npm run test:api` after the route/UI changes.

## UI notes
- Keep the dashboard label as `AutoClipper` so users see the new engine name.
- Show concrete pipeline stages such as runtime check, metadata selection, clip target duration, and subtitle export.
- Keep output parsing deduplicated so repeated worker outputs do not render duplicate links.

## Pitfalls
- Do not hardcode secrets in the worker or route.
- Do not assume the upstream repo is a drop-in Node package; treat it as a Python runtime dependency source.
- Prefer vendor/runtime copying over importing directly from the clone path.
- If the route still mentions the old `Youtube-clipper-skill` copy, patch the visible strings and engine metadata together so UI and backend stay aligned.
