# YouTube clipper yt-dlp cookies/login block

Context: Dockerized React/Express app with an auth-protected Auto Clipper endpoint that shells out to `vendor/youtube-clipper-skill` Python scripts. Some YouTube URLs work publicly, while others fail only in production/headless server environments.

## Root-cause pattern

When a clipper job fails at the `download` stage, inspect persisted job logs/stages first instead of patching from the UI symptom. In this repo the DB table `clipper_jobs` contained the real yt-dlp error:

```text
Sign in to confirm you’re not a bot. Use --cookies-from-browser or --cookies for the authentication...
```

This is not a generic server crash. It means YouTube is blocking the server/headless downloader for that video or IP/session, and some videos require authenticated cookies while public videos may still work.

## Durable fix pattern

In the Python downloader (`vendor/youtube-clipper-skill/scripts/download_video.py`):

- Read a Netscape-format cookies path from env, with a persistent default:
  - `YT_DLP_COOKIES_FILE`
  - `YOUTUBE_COOKIES_FILE`
  - `/app/data/youtube-cookies.txt`
- Only set `ydl_opts['cookiefile']` when the file exists.
- Print whether cookies are active or missing, but never print cookie contents.
- Add browser-like headers, retry/timeouts, and a YouTube player client fallback to reduce false bot blocks.

Representative options:

```python
cookie_file = os.environ.get('YT_DLP_COOKIES_FILE') or os.environ.get('YOUTUBE_COOKIES_FILE') or '/app/data/youtube-cookies.txt'
cookie_path = Path(cookie_file).expanduser() if cookie_file else None

ydl_opts = {
    'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
    'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'subtitlesformat': 'vtt',
    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    },
    'retries': 3,
    'fragment_retries': 3,
    'socket_timeout': 30,
}

if cookie_path and cookie_path.exists():
    ydl_opts['cookiefile'] = str(cookie_path)
```

In the Express route (`src/routes/clipper.ts`), convert the raw yt-dlp bot/cookie text into a clear user-facing error:

- Detect `/Sign in to confirm|not a bot|cookies/i` in the download log.
- Store an actionable Indonesian message explaining that YouTube blocked the server and that a Netscape cookies file must be uploaded to `/app/data/youtube-cookies.txt` or configured via `YT_DLP_COOKIES_FILE`.
- Include only a bounded tail of the raw detail; never echo credentials.

## Verification pattern

Use two production smoke cases:

1. Known public video, to prove the pipeline still works without cookies.
   - Expected: job reaches `downloaded` or the app's intended success status and has output files.
2. Problematic user video, to prove the error message is now clear.
   - Expected without cookies: job fails with the actionable cookies/login message, not a generic “failed”.

Also verify:

```bash
npm run build:server
npx cross-env NODE_ENV=test DATABASE_FILE=/tmp/nusantara-ai-test.db JWT_SECRET=[REDACTED] jest --config jest.config.cjs --runInBand tests/api
bash scripts/deploy.sh
curl -fsS https://<domain>/api/health
```

## Ops guidance

- Do not ask the user to paste cookies, passwords, or tokens into chat.
- Treat YouTube cookies as credentials.
- Upload the Netscape cookies file directly to the server path that maps to `/app/data/youtube-cookies.txt` and restrict permissions, for example `chmod 600`.
- If using the default path, no code change is needed; the downloader checks for the file on each run.
- Do not claim this bypasses every YouTube restriction. It enables the standard yt-dlp authenticated-cookie path; YouTube may still rate-limit or block sessions.
