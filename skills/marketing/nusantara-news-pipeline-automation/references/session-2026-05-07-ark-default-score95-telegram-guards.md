# Session Notes: Ark default, 95+ single-item threshold, Telegram guards

Date: 2026-05-07

Key operational learnings from this session:

- Default provider for both image and video generation should be Ark unless the user explicitly overrides it.
- When a run is configured to send to Telegram, skip the send for any item missing its required files instead of pushing partial media.
  - Image delivery requires the rendered image file to exist.
  - Video delivery requires both the reference image and final video file to exist.
  - Prefer explicit skip reasons such as `missing image`, `missing video`, or `missing both`.
- For single-news runs (`--count 1` / one-item mode), enforce a minimum score threshold of 95+ and fail early if no candidate meets it.
- Keep the threshold configurable via env when useful, but default it to 95.
- After any scoring or provider change, run a dry-run and verify the manifest actually reflects the new provider and threshold behavior.
