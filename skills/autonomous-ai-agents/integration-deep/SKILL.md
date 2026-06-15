---
name: integration-deep
description: "Use when performing deep integration work across codebases, modules, or agentic-flow components with focused interface and dependency analysis."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [integration, deep, modules, dependencies, interfaces, ruvector]
    related_skills: [v3-integration-deep, claude-core, architecture-system-design, claude-analysis]
---

# Integration Deep

## Overview

Use this skill when a task needs deep integration across modules, services, or agentic-flow components.
It is a compact reference for interface alignment, dependency analysis, and integration-safe changes.

## When to Use

Use when you need to:

- integrate multiple modules or services
- reason about dependencies and interface boundaries
- validate end-to-end behavior after integration
- coordinate deep changes that cross subsystem lines

Do not use for:

- isolated single-file edits
- pure architecture discussion without implementation
- unrelated analysis tasks

## Integration Focus

- interface compatibility
- dependency mapping
- data flow across components
- integration test coverage
- regression risk during merge

## Usage Notes

- Map dependencies before changing code.
- Keep interfaces stable where possible.
- Validate both sides of the integration boundary.
- Check for hidden coupling and side effects.

## Common Pitfalls

1. Changing one side of an interface without checking the other.
2. Ignoring integration tests until after merge.
3. Missing transitive dependencies.
4. Treating integration as just a code patch.

## Verification Checklist

- [ ] Dependencies mapped
- [ ] Interfaces checked
- [ ] Integration path validated
- [ ] Regression risk considered
- [ ] End-to-end behavior verified
