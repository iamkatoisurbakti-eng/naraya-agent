---
name: worker-multi
description: "Use when coordinating multiple workers on one task, splitting work across parallel worker roles, and merging their outputs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [workers, multi-worker, parallel, coordination, merge]
    related_skills: [worker-integration, worker-benchmarks, claude-flow-background-workers]
---

# Worker Multi

## Overview

Use this skill when one task should be split across multiple workers and merged back into a single result.
It helps coordinate parallel work without losing the final synthesis.

## When to Use

Use when you need to:

- split a task into parallel worker parts
- assign different focus areas to different workers
- merge partial results into one answer
- reduce time by working in parallel

## Notes

- Keep worker roles narrow.
- Define one synthesis point.
- Reconcile overlaps before final output.

## Checklist

- [ ] Work split cleanly
- [ ] Roles are distinct
- [ ] Results merged once
- [ ] Final synthesis is clear
