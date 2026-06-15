# KSR888 Growth Automation Trio

Session pattern for nonstop KSR888 growth operations.

Goal
- Keep SEO, indexing, content/publishing, and mobile UX work running in parallel without overlap.
- Use staggered schedules so each run has a distinct lane and the reports stay readable.
- Prefer one job per theme; do not stack multiple jobs for the same purpose unless there is a clear difference in output.

Observed clean schedule pattern
- 00 minute: SEO multi-agent
- 05 minute: indexing multi-agent
- 15 minute: AMP multi-agent
- 30 minute: content/publishing
- 45 minute: mobile UX multi-agent

Rules that worked well
1. Start from the live job list before creating anything new.
2. Remove duplicate or redundant jobs before renaming or rescheduling.
3. Use exact offsets to prevent tabling collisions in the same hour.
4. Keep the mobile UX loop hourly when the request says 24 jam nonstop.
5. Verify with a fresh `cronjob list` after every create/update/remove batch.
6. If a user asks for the “most clean” schedule, prefer fewer themes with consistent offsets over many similar jobs.

What to watch for
- Overlapping SEO/marketing jobs can produce duplicate findings.
- Mobile UX work should stay on a short interval if the user wants continuous polish.
- Indexing and SEO are close enough to overlap conceptually, so their prompts must make the split explicit.
- AMP is a separate lane only if the site actually has an AMP surface; otherwise treat it as optional.
