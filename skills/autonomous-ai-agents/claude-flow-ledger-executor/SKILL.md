---
name: claude-flow-ledger-executor
description: "Use when enforcing the claude-flow ledger/executor split, including memory-first planning and post-success pattern storage."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [claude-flow, ledger, executor, memory, patterns, workflow]
    related_skills: [claude-flow-workflows, claude-flow-rolechains, claude-flow-background-workers, reasoningbank]
---

# Claude Flow Ledger / Executor Split

## Overview

Use this skill when claude-flow should act as the ledger and Hermes should act as the executor.
It defines the operating split between state tracking and action execution.

## Rules

1. claude-flow is the LEDGER.
   - tracks state
   - stores memory
   - coordinates work

2. Hermes is the EXECUTOR.
   - writes code
   - runs commands
   - creates files

3. Never stop after calling claude-flow.
   - continue working immediately

4. If something must be built or executed, do it directly.
   - do not hand execution off

5. Search memory before starting.
   - look for related prior patterns first

6. Store patterns after success.
   - record reusable patterns once the task works

## Usage Notes

- Use memory search before implementation.
- Keep claude-flow focused on coordination and state.
- Keep Hermes focused on execution and delivery.
- Save successful patterns after verification.

## Common Pitfalls

1. Treating claude-flow as the builder instead of the ledger.
2. Forgetting to search memory before starting.
3. Completing a task without storing the useful pattern.
4. Stopping after planning instead of executing.

## Verification Checklist

- [ ] Memory was searched first
- [ ] Execution was done directly
- [ ] claude-flow was used only for state/coordination
- [ ] Successful pattern was stored
