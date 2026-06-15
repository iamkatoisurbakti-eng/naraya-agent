---
name: multi-agent-self-evaluation
description: "Use when multiple agents must evaluate their own outputs, compare results, and decide whether to revise or accept work."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [multi-agent, self-evaluation, review, scoring, verification, coordination]
    related_skills: [claude-consensus, claude-analysis, claude-flow-ledger-executor, verification-quality]
---

# Multi-Agent Self Evaluation

## Overview

Use this skill when several agents need to evaluate their own work or each other's outputs.
It supports scoring, comparison, and revision decisions.

## When to Use

Use when you need to:

- score agent outputs
- compare multiple solutions
- decide whether to revise or accept work
- produce a concise evaluation summary

Do not use for:

- direct execution tasks
- one-agent trivial work
- memory consolidation or retrieval only

## Evaluation Flow

1. Collect outputs.
2. Score each output against the goal.
3. Compare strengths and weaknesses.
4. Choose accept, revise, or reject.
5. Record the reason for the decision.

## Usage Notes

- Use explicit criteria.
- Keep scoring simple and consistent.
- Note both correctness and completeness.
- Separate subjective preference from objective quality.

## Common Pitfalls

1. Scoring without a shared rubric.
2. Confusing style with correctness.
3. Skipping revision when outputs are weak.
4. Treating self-evaluation as final truth.

## Verification Checklist

- [ ] Outputs collected
- [ ] Shared criteria used
- [ ] Decision made clearly
- [ ] Revision path noted if needed
- [ ] Final evaluation is concise
