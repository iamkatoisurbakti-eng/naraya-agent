---
name: claude-flow-rolechains
description: "Use when coordinating multi-stage bugfix, feature, refactor, performance, security, or memory workflows with coordinator-led role chains."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [workflow, orchestration, bugfix, feature, refactor, performance, security, memory]
    related_skills: [claude-flow-workflows, swarm-advanced, hive-mind, memory-management, verification-quality]
---

# Claude Flow Role Chains

## Overview

Use this skill when a task should be split into a coordinator-led role chain.
Each workflow keeps the stages short, explicit, and verifiable.

## When to Use

Use for:

- bug investigation and fix
- feature development
- refactoring and modernization
- performance tuning
- security review
- memory-related optimization

Do not use for:

- one-step edits
- trivial text changes
- work that does not need handoff or verification

## Workflow Templates

### 1. Bug Fix

Flow:

- Coordinator → Researcher → Coder → Tester

Use when you need to reproduce, isolate, patch, and verify a bug.

### 3. Feature

Flow:

- Coordinator → Architect → Coder → Tester → Reviewer

Use for full feature delivery with design, implementation, validation, and review.

### 5. Refactor

Flow:

- Coordinator → Architect → Coder → Reviewer

Use for code modernization or structural cleanup.

### 7. Performance

Flow:

- Coordinator → Perf-Engineer → Coder

Use when the goal is to profile, optimize, and implement performance improvements.

### 9. Security

Flow:

- Coordinator → Security-Architect → Auditor

Use for security hardening, threat modeling, and audit reporting.

### 11. Memory

Flow:

- Coordinator → Memory-Specialist → Perf-Engineer

Use when the task involves memory coordination, retrieval, or optimization.

### 13. Docs

Flow:

- Researcher → Api-Docs

Use when the task is about API documentation, reference writing, or docs cleanup.

## Execution Notes

- Start with the coordinator to set scope and handoff order.
- Keep each role focused on a single output.
- Test or audit before marking the work done.
- If the first pass is unclear, rerun the coordinator before coding.

## Common Pitfalls

1. Skipping the coordinator and letting roles blur together.
2. Ending after code changes without testing or review.
3. Using the performance or memory workflows for unrelated tasks.
4. Overloading one role with too many responsibilities.

## Verification Checklist

- [ ] Correct workflow chosen
- [ ] Coordinator assigned first
- [ ] Roles are in the right order
- [ ] Verification step included
- [ ] Final result is ready to hand off
