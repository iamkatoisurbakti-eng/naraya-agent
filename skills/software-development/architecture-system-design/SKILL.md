---
name: architecture-system-design
description: "Use when designing system architecture, defining components, APIs, data flow, scalability, and trade-offs before implementation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [architecture, system-design, scalability, tradeoffs, api, components]
    related_skills: [writing-plans, requesting-code-review, test-driven-development]
---

# Architecture / System Design

## Overview

Use this skill when a project needs a clear system design before coding.
It helps define components, boundaries, data flow, scaling strategy, and trade-offs.

## When to Use

Use when you need to:

- design a new system or major feature
- split a feature into components
- choose between architecture options
- define APIs, storage, queues, and deployment shape
- reason about performance, reliability, and maintainability

Do not use for:

- tiny bug fixes
- trivial text or config edits
- tasks that already have a locked design

## Design Checklist

- What problem is the system solving?
- What are the main components?
- What owns the data?
- How do services communicate?
- What are the scaling bottlenecks?
- What are the failure modes?
- What trade-offs are being made?

## Output Shape

A good architecture answer usually includes:

- goals and constraints
- high-level component map
- data flow
- API boundaries
- storage choices
- scaling and reliability notes
- trade-offs and risks

## Common Pitfalls

1. Jumping into code before defining boundaries.
2. Ignoring failure modes and retries.
3. Skipping trade-offs.
4. Making the design too abstract to implement.

## Verification Checklist

- [ ] Problem statement is clear
- [ ] Components and boundaries are defined
- [ ] Data flow is mapped
- [ ] Trade-offs are explicit
- [ ] Design is implementation-ready
