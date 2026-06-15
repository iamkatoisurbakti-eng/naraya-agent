# Session note: Gen-Z KBBI style + video title overlay

Date: 2026-05-07

## What changed
- Default template for the Gen-Z news workflow can be overridden with `/root/template-genz-news.html`.
- A separate video post-process was added to burn the article title onto generated MP4s.
- Output caption style was updated from `Hook:` / `Viral momentum:` to:
  - `Judul: ...`
  - `Inti cerita: ...`
- Hashtags were localized to Indonesian-facing tags.

## Commands
From `/root/nusantara-ai-saas`:

```bash
npm run gen:viral-news -- --count 1 --dry-run --template /root/template-genz-news.html
npm run gen:viral-news:video-titles -- --video-manifest <path>/video-manifest.json --template /root/template-genz-news.html
```

## Pitfall
- The first ffmpeg `drawtext` attempt failed because an overlay note was accidentally inserted into the filter string. Keep the title overlay filter minimal and valid.

## Verification
- Confirm `video-title-manifest.json` is written.
- Confirm titles are visible in the resulting MP4s.
- Confirm dry-run manifest captions still render correctly in Indonesian/KBBI style.
