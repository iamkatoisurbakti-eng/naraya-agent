---
name: senior-developer
description: "Use when solving software problems with senior-level judgment: architecture, code quality, debugging, trade-offs, and delivery readiness."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [senior, developer, engineering, architecture, debugging, quality, delivery]
    related_skills: [architecture-system-design, systematic-debugging, test-driven-development, requesting-code-review]
---

# Senior Developer

## Overview

Use this skill when a task requires strong engineering judgment rather than just implementation speed.
It applies senior-level thinking to architecture, code quality, debugging, trade-offs, and delivery.

## When to Use

Use when you need to:

- choose between implementation approaches
- review or improve existing code
- debug hard or ambiguous issues
- design maintainable systems
- balance speed, quality, and risk
- prepare work for production delivery

## Working Style

1. Understand the problem and constraints first.
2. Identify the smallest safe change.
3. Favor clarity and maintainability.
4. Check edge cases and failure modes.
5. Verify the result with tests or live checks.

## Senior-Level Heuristics

- Prefer simple, explicit solutions over clever ones.
- Reduce coupling and hidden state.
- Make behavior observable and testable.
- Choose correctness before optimization unless performance is the problem.
- Preserve user-facing stability unless a change is clearly worth it.

## Common Pitfalls

- Overengineering a small problem.
- Shipping a fix without understanding the root cause.
- Ignoring tests, observability, or rollback paths.
- Optimizing before the design is stable.

## Verification Checklist

- [ ] Problem and constraints are understood
- [ ] The chosen approach is justified
- [ ] Edge cases were considered
- [ ] Verification was performed
- [ ] The result is maintainable
