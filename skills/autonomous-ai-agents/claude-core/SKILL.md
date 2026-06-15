---
name: claude-core
description: "Use when applying the core Claude Flow primitives for state, coordination, memory, routing, and execution boundaries."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [claude, core, coordination, memory, routing, execution]
    related_skills: [claude-flow-ledger-executor, claude-consensus, claude-analysis, reasoningbank]
---

# Claude Core

## Overview

Use this skill when you need the core Claude Flow mental model:
state tracking, coordination, memory, routing, and clean execution boundaries.
It is the base reference for how Claude-oriented workflows should behave.

## When to Use

Use when you need to:

- define the core workflow model
- separate ledger/state from executor/action
- route work through the right primitives
- keep memory and execution responsibilities distinct

Do not use for:

- detailed implementation of a specific workflow
- one-off coding tasks
- tasks that already fit a more specific skill

## Core Principles

- Track state before acting.
- Use coordination to organize work.
- Keep memory reusable and structured.
- Execute directly when action is needed.
- Prefer small, verifiable steps.

## Usage Notes

- Start with the goal and state.
- Pick the smallest useful primitive.
- Store useful patterns after success.
- Avoid mixing planning, memory, and execution in one step.

## Common Pitfalls

1. Treating core coordination as a replacement for execution.
2. Skipping memory and state tracking.
3. Using a narrow workflow when the core model is needed.
4. Failing to distinguish routing from implementation.

## Verification Checklist

- [ ] State is clear
- [ ] Coordination path is defined
- [ ] Memory is structured
- [ ] Execution boundary is explicit
- [ ] Workflow is ready to run
