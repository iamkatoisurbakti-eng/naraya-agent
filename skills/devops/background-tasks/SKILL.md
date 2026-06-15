---
name: background-tasks
description: "Use when starting, monitoring, or managing long-running work in the background without blocking the current session."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [background, tasks, long-running, process, monitoring, async, jobs]
    related_skills: [workflow-automation, claude-flow-background-workers, scheduler-agent]
---

# Background Tasks

## Overview

Use this skill when work should continue asynchronously while the user keeps chatting or you continue other tasks.

## When to Use

Use when you need to:

- run a server, watcher, or daemon
- execute a long test/build/deploy job
- monitor a process until completion
- queue work that should not block the session
- capture output when a background job finishes

## Working Style

1. Start the job in a managed background process.
2. Verify it is running and healthy.
3. Poll logs only when needed.
4. Prefer a completion notification for finite jobs.
5. Use a quiet watchdog pattern for recurring checks.

## Common Patterns

- Long build or test: start in background, notify on completion.
- Server startup: wait for readiness signal, then verify endpoint.
- If the server binds to a fixed port, check for an existing listener first (`ss -ltnp`, `lsof -i`) and decide whether to reuse, stop, or move the port before launching a new process.
- Watchdog task: keep it quiet unless a threshold is crossed.
- Batch job: collect output, then summarize results for the user.

## Server Start Verification

When starting a web server in the background:
1. Confirm the port is free or identify the existing PID.
2. Start the server as a managed background process.
3. Verify readiness with a lightweight health endpoint rather than trusting process startup alone.
4. If startup fails with `address already in use`, treat it as a port-collision workflow problem, not an app failure.

## Common Pitfalls

- Using background mode for work that should be synchronous.
- Forgetting to verify readiness before assuming success.
- Spamming log checks instead of waiting for completion.
- Writing noisy watchdogs that report constantly.

## Verification Checklist

- [ ] The task is truly asynchronous
- [ ] The process/job was started correctly
- [ ] Readiness or completion was verified
- [ ] Output was captured or summarized
