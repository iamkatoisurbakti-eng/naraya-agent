---
name: autonomous-optimization-architect
description: "Use when designing autonomous optimization systems for agents, workflows, routing, memory, performance, and continuous improvement loops."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [autonomous, optimization, architecture, agents, routing, memory, performance, improvement]
    related_skills: [performance-analysis, memory-management, reasoningbank, agent-coordination, ai-engineer]
---

# Autonomous Optimization Architect

## Overview

Use this skill when building systems that improve themselves over time: routing, memory, performance tuning, feedback loops, and adaptive orchestration.

## When to Use

Use when you need to:

- design self-improving agent systems
- optimize workflows or orchestration logic
- add feedback loops for routing or memory
- reduce cost, latency, or wasted work
- choose where automation should adapt versus stay fixed
- define metrics for continuous improvement

## Working Style

1. Define the optimization target clearly.
2. Identify the measurable bottleneck.
3. Add feedback and evaluation loops.
4. Keep the architecture simple enough to observe.
5. Verify improvements with repeatable checks.

## Core Concerns

- Agent routing and task assignment
- Memory retention and recall quality
- Performance, latency, and cost
- Learning from outcomes and failures
- Stability under changing conditions
- Guardrails against runaway complexity

## Common Patterns

- feedback-driven routing
- adaptive worker selection
- memory-backed pattern reuse
- quality scoring and rollback
- performance dashboards and thresholds
- staged optimization: observe → adjust → verify

## Common Pitfalls

- Optimizing without a metric.
- Adding learning loops before the base system is stable.
- Making the optimizer more complex than the system it tunes.
- Confusing experimentation with production behavior.

## Verification Checklist

- [ ] The optimization target is measurable
- [ ] The bottleneck is identified
- [ ] The improvement path is simple and testable
- [ ] Feedback loops are bounded
- [ ] Verification shows the change actually helps
