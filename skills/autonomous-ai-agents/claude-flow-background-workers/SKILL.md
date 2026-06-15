---
name: claude-flow-background-workers
description: "Use when coordinating Claude Flow background workers for trigger-based agent dispatch, memory coordination, and performance tracking."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [workers, background, triggers, dispatch, memory, performance]
    related_skills: [worker-integration, worker-benchmarks, claude-flow-hooks, claude-flow-rolechains, memory-management]
---

# Claude Flow Background Workers

## Overview

Use this skill as a compact reference for the background worker layer.
It summarizes the worker triggers, the typical agent routing, and the core purpose of the worker system.

## When to Use

Use when you need to:

- map trigger words to worker behavior
- route work to the right agents
- track worker performance or memory patterns
- benchmark the worker system

Do not use for:

- one-off agent tasks without trigger routing
- full workflow orchestration
- implementation details of the worker runtime

## Core Worker Triggers

| Trigger | Primary Agents | Purpose |
|---|---|---|
| ultralearn | researcher, coder | Deep knowledge acquisition |
| optimize | performance-analyzer, coder | Performance optimization |
| audit | security-analyst, tester | Security review |
| benchmark | performance-analyzer | Measurement and reporting |
| testgaps | tester | Coverage discovery |
| document | documenter, researcher | API docs and indexing |
| deepdive | researcher, security-analyst | Investigation and tracing |
| refactor | coder, reviewer | Code modernization |

## Worker System Notes

- Workers automatically dispatch based on trigger type.
- Memory keys typically follow `{trigger}/{topic}/{phase}`.
- Performance monitoring should track latency, success rate, and quality score.
- Benchmarking should validate trigger detection, registry operations, agent selection, and concurrent worker behavior.

## Common Pitfalls

1. Treating workers like ordinary one-off agent calls.
2. Forgetting to route by trigger before selecting an agent.
3. Ignoring memory key consistency.
4. Measuring worker quality without checking latency and success rate.

## Verification Checklist

- [ ] Trigger identified correctly
- [ ] Agent routing selected
- [ ] Memory pattern is consistent
- [ ] Performance impact considered
- [ ] Worker output is verified
