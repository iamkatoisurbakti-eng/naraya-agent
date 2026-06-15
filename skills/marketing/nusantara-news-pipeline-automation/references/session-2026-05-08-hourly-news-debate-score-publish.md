# Session note: hourly news debate/score/publish cron

Observed in this session:

- A new recurring automation was created for Nusantara-AI News with a 60m schedule.
- The prompt combined four classes of skills:
  - `cnnindonesia-news-api` for fetching recent news candidates
  - `content-ideation-agent` for debating/testing/voting/scoring candidates
  - `nusantara-news-pipeline-automation` for HTML/PNG/Shorts asset generation
  - `scheduler-agent` for Telegram delivery and publish orchestration
- The intended output was a single selected story plus:
  - `flyer-[TANGGAL_ISO].html`
  - `video-[TANGGAL_ISO].html`
  - rendered flyer PNG 4:5
  - Telegram delivery to the active home channel
- The verification step that mattered was `cronjob list` after creation; it confirmed the job count, `job_id`, schedule, and enabled state.

Practical takeaway:

- For a new recurring news automation, the safest default is a single composite cron job that covers fetch → score → render → deliver, then verify it immediately with `cronjob list`.
- If the user wants Telegram delivery, make the prompt explicit about the target channel/chat and the requirement to verify file dimensions before send.
- Keep prompt text in the job concise enough that the preview remains readable, but do not omit the asset/output contract.
