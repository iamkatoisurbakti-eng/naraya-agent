---
name: claude-flow-workflows
description: "Use when coordinating feature, security, refactor, or bugfix work across architect, coder, tester, reviewer, scanner, or reporter stages."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, workflow, orchestration, feature-development, security-audit, refactor, bugfix]
    related_skills: [swarm-advanced, hive-mind, memory-management, workflow-automation, verification-quality]
---

# Claude Flow Workflows

## Overview

Use this skill to turn a goal into a short, repeatable multi-stage workflow.
It covers four common patterns:

- feature development
- security audit
- code modernization / refactor
- bug investigation and fix

Each pattern uses a small role chain with a clear handoff between stages.

## When to Use

Use when the task needs more than one pass, especially if you want:

- clear role separation
- verification before delivery
- security review or scanning
- structured handoff between planning, implementation, and testing

Do not use for:

- one-line edits
- trivial config changes
- tasks that do not need review or testing

## Workflow Templates

### 1) Feature

Flow:

- 🔵 Architect → 🟢 Coder → 🔵 Tester → 🟢 Reviewer

Use for full feature development.

Suggested responsibilities:

- Architect: define scope, API, and implementation plan
- Coder: implement the feature
- Tester: verify behavior and edge cases
- Reviewer: check quality, readability, and regressions

### 2) Security

Flow:

- 🔵 Analyst → 🟢 Scanner → 🔵 Reporter

Use for security audit work.

Suggested responsibilities:

- Analyst: identify attack surface and risks
- Scanner: run checks, grep patterns, and validation
- Reporter: summarize findings and severity

### 3) Refactor

Flow:

- 🔵 Architect → 🟢 Refactorer → 🔵 Tester

Use for code modernization.

Suggested responsibilities:

- Architect: define target structure and migration path
- Refactorer: reshape code without changing behavior
- Tester: confirm behavior stays intact

### 4) Bugfix

Flow:

- 🔵 Researcher → 🟢 Coder → 🔵 Tester

Use for bug investigation and fix.

Suggested responsibilities:

- Researcher: reproduce, isolate, and identify root cause
- Coder: apply the fix
- Tester: verify the fix and check regressions

## Execution Notes

- Keep each stage small and explicit.
- Do not skip tester/reviewer stages on risky work.
- If the first pass is unclear, re-run the architect/researcher stage before coding.
- Write down assumptions before implementation.
- Prefer verification by tests, logs, or direct inspection.

## Common Pitfalls

1. Skipping the architect/research stage and jumping straight to code.
2. Treating reviewer/scanner as optional on security-sensitive work.
3. Letting the coder and tester overlap without a clean handoff.
4. Not restating the goal before each stage.
5. Forgetting to verify the final result after implementation.

## Verification Checklist

- [ ] The workflow type is chosen correctly
- [ ] Roles are assigned in order
- [ ] Implementation is followed by verification
- [ ] Findings or fixes are summarized clearly
- [ ] The result is ready for handoff or delivery
