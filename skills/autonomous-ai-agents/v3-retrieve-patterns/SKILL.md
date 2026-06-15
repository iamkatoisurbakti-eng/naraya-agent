---
name: v3-retrieve-patterns
description: "Use when retrieving relevant patterns via HNSW for rapid memory lookup and pattern recall."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [retrieve, hnsw, patterns, memory, recall, search]
    related_skills: [v3-ruvector-intelligence-system, claude-flow-intelligence-routing, memory-management]
---

# Retrieve Patterns via HNSW

## Overview

Use this skill when the task needs fast retrieval of relevant patterns, examples, or memories.
It focuses on HNSW-backed search for high-speed recall.

## When to Use

Use when you need to:

- fetch relevant patterns from memory
- recall prior solutions quickly
- search for similar workflows or examples
- support routing decisions with prior evidence

Do not use for:

- writing new code from scratch without lookup
- final verification or judgment
- memory consolidation

## RETRIEVE

Purpose: fetch relevant patterns via HNSW.

Typical outputs:

- nearest matches
- similar examples
- reusable patterns
- short retrieval summary

## Usage Notes

- Use RETRIEVE before deciding on implementation details.
- Prefer it when prior examples matter more than fresh exploration.
- Keep the retrieved set small and relevant.

## Common Pitfalls

1. Retrieving too many weak matches.
2. Using retrieval as a substitute for judgment.
3. Forgetting to narrow by task topic.

## Verification Checklist

- [ ] Relevant patterns retrieved
- [ ] Search was narrow enough
- [ ] Results are ready for downstream use
