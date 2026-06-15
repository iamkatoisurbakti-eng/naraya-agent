# News pipeline notes

Session takeaways for the unified Nusantara AI news pipeline.

## Current orchestration
- Primary command: `npm run gen:news-pipeline -- --count <N>`
- Per generated story, the pipeline produces exactly two public media outputs:
  - one 5:4 Instagram image export under `instagram-5x4/`
  - one short-form video export (raw video + title-burned final video), with the full-run target set to at least 30 seconds
- The image stage runs first and its output becomes the reference image for the video stage.
- The pipeline also writes article output under `/news/<category>/<slug>`, optional YouTube Shorts upload manifests, optional Telegram delivery, and final `pipeline-report.json` and `pipeline-report.md`.

## Caption requirements
- Every story caption should include:
  - `Judul: ...`
  - `Hook viral: ...`
  - `Inti cerita: ...`
  - a short CTA
  - hashtags
- Keep the Instagram and YouTube captions separate in the manifest even if they are derived from the same story.
- Hashtags should always include `#HookViral` so the viral hook is explicit.

## Instagram image export
- Treat Instagram as a dedicated 5:4 output, not a copy of the video artifact.
- Use separate manifest naming for the image pack so it is obvious in reports and downstream delivery.
- Keep the image artifact and the short video artifact independent so one can succeed even if the other stage is skipped.

## Video export
- Shorts should be generated separately from Instagram images.
- The Instagram image URL/path should be passed as the video reference image.
- The title-burned MP4 should carry an audio stream when the workflow asks for audio output.
- Verify audio presence with `ffprobe -select_streams a:0` before upload or delivery.

## Reporting
- A complete report should list, per item:
  - article URL
  - Instagram 5:4 image path
  - reference image URL
  - raw video path
  - final short video path
  - YouTube URL if uploaded
  - Telegram status
- If the user asks for a “complete pipeline” or “full publish”, end the run with a machine-readable report and a readable markdown report.
