# Production Log Audit (24h)

Use this when auditing a containerized web app for errors in the last 24 hours.

## Scope
- Collect only evidence from the last 24h first.
- Separate app logs, reverse-proxy logs, and health checks.
- Prefer live verification over assumptions.

## Recommended probes
- `docker logs --since 24h <app-container>`
- `docker logs --since 24h <proxy-container>`
- Health endpoints (`/api/health`, root page, critical assets)
- If relevant, inspect restart timing / deploy timing before calling a failure real.

## Triage rules
- Treat `http2: stream closed`, incomplete response, or client disconnects as noise unless they repeat after stable uptime and correlate with a user-visible failure.
- Treat DNS lookup / upstream misbehavior during container restart or reload as transient unless it persists after the service settles.
- Only patch code when the same user-visible error is reproducible or clearly tied to a source-level defect.

## Output checklist
- What logs were checked
- What endpoints were verified
- Whether the issue is transient or code-level
- Exact files changed, if any
- Minimal verification after any patch