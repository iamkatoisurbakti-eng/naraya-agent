# Session note: berita-daily hourly Telegram export

Use the user-maintained prompt file `/root/.hermes/berita-daily.txt` as the editorial source when the user asks to "jalankan /root/.hermes/berita-daily.txt" or to re-run the daily berita automation.

## Reusable run shape
- Read the prompt file first, then execute the automation with the same editorial constraints.
- Produce exactly one package per run unless the user explicitly asks for batch mode.
- Required deliverables:
  - 1 flyer PNG in 4:5 format
  - 1 short video MP4 in 9:16 format
  - complete caption
  - exactly 4 hashtags
- Delivery target: Telegram
- Schedule: run immediately, then repeat every 60 minutes

## Cron-job pattern discovered
The cron API accepted this style of job creation for the hourly automation:
- `schedule: every 60m`
- `repeat: forever`
- `deliver: origin`
- `workdir: /root/nusantara-ai-saas`
- `skills: ["nusantara-news-pipeline-automation"]`

After creation, the job can be triggered immediately with a separate run action.

## Pitfalls
- Do not post partial output. If either the flyer PNG or short MP4 is missing, skip the send and report failure.
- Keep the Telegram caption complete; no ellipses or truncated fragments.
- Keep the hashtag count fixed at 4 unless the user explicitly changes the requirement.
