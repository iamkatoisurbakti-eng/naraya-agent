# Session Note: Cron `run` Is Not a Guaranteed Immediate Execute

## What was observed

When using Hermes cron jobs, `cronjob run <job_id>` may update the schedule metadata and move `next_run_at`, but it does **not** always mean the underlying automation has already produced output or delivered Telegram media.

Observed behavior in this session:
- `cronjob run` returned success for the scheduled job.
- `last_run_at` remained `null` immediately afterward.
- `next_run_at` moved to the near future.
- No actual content run had been verified yet.

## Practical rule

Treat `cronjob run` as a *trigger request*, not proof of completion.

Before telling the user that a test run completed, verify at least one of:
- the runner/process actually started and produced artifacts,
- the run directory exists and contains expected files,
- the queue/state log shows the slot executed,
- Telegram delivery success is recorded.

## Recommended verification checklist

1. Inspect the cron job state again after the trigger.
2. Confirm `last_run_at` and `last_status` changed if the cron system reports them.
3. Check the run directory for generated HTML/PNG/MP4 assets.
4. Check the pipeline or queue log for the actual execution.
5. Confirm Telegram send success only after the send call itself succeeds.

## Telegram target caution

When a job says it will send to Telegram, verify the exact target mapping first.
A bare `telegram` destination may resolve to a home channel or mirrored target instead of the intended public channel.

## Takeaway for Scheduler Agent

If the user asks for **"run sekali sekarang"**, do not rely on `cronjob run` alone. Use the actual runner/pipeline when possible, then verify files and delivery before reporting success.
