# Cronjob stop/pause/remove notes (2026-05-08)

Observed workflow for Hermes cron jobs:

- `action: list` returns all jobs, including paused ones.
- `action: pause` is enough to stop a job temporarily; it flips `enabled=false` and `state=paused`.
- `action: remove` deletes the job permanently.
- After bulk removals, re-run `list` to verify the job count is zero.

Practical use:
- For `stop automation`, pause the active job first, then remove it if the user wants it gone permanently.
- For `hapus semua paused`, enumerate paused jobs from `list`, remove each one, then confirm an empty list.
- Do not assume a job is gone until a follow-up `list` confirms it.
