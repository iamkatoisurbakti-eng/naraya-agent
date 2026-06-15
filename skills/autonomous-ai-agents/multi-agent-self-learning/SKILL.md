---
name: multi-agent-self-learning
description: "Use when coordinating multiple agents that learn from outcomes, share memory, and improve routing or task performance over time."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [multi-agent, self-learning, memory, routing, coordination, adaptation]
    related_skills: [claude-flow-background-workers, claude-flow-ledger-executor, reasoningbank, sona-learning]
---

# Multi-Agent Self Learning

## Overview

Use this skill when multiple agents need to collaborate, learn from results, and improve future behavior.
It combines coordination, shared memory, and incremental adaptation.

## When to Use

Use when you need to:

- coordinate more than one agent
- capture feedback from task outcomes
- improve routing or role assignment over time
- share learnings across repeated runs

Do not use for:

- single-agent tasks
- one-off actions with no reusable learning
- simple execution without feedback loops

## Core Loop

1. Assign agents and roles.
2. Execute the task.
3. Collect outcome signals.
4. Store reusable patterns.
5. Adjust future routing or behavior.

## Usage Notes

- Keep learning signals small and structured.
- Record both success and failure patterns.
- Share only stable learnings with future runs.
- Prefer incremental updates over broad rewrites.

## Common Pitfalls

1. Learning from unverified results.
2. Overwriting stable patterns too aggressively.
3. Using too many agents without clear roles.
4. Forgetting to store useful outcomes after success.

## Verification Checklist

- [ ] Agents have clear roles
- [ ] Outcome signals were collected
- [ ] Useful patterns were stored
- [ ] Future routing can improve
- [ ] Learning remains incremental
