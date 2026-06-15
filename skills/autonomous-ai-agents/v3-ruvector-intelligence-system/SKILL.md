---
name: v3-ruvector-intelligence-system
description: "Use when applying the RuVector Intelligence System for verdict evaluation, key learning distillation, and memory consolidation to reduce catastrophic forgetting."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ruvector, intelligence-system, judge, distill, consolidate, lora, ewc, memory]
    related_skills: [claude-flow-intelligence-routing, claude-flow-background-workers, memory-management, verification-quality]
---

# RuVector Intelligence System

## Overview

Use this skill when a workflow needs three intelligence stages:

- JUDGE: evaluate with verdicts
- DISTILL: extract key learnings via LoRA
- CONSOLIDATE: prevent catastrophic forgetting via EWC++

This is a compact reference for turning raw execution results into verdicts, reusable learning, and stable memory.

## When to Use

Use when you need to:

- score or judge task outcomes
- extract reusable knowledge from successful runs
- consolidate memory so later work does not forget earlier lessons
- keep multi-run agent behavior stable over time

Do not use for:

- single-step edits
- tasks that do not produce reusable learnings
- ordinary implementation work without evaluation

## Stages

### JUDGE

Purpose: evaluate with verdicts.

Typical outputs:

- success / failure
- quality score
- confidence
- short rationale

Use JUDGE after execution to decide whether the work is acceptable.

### DISTILL

Purpose: extract key learnings via LoRA.

Typical outputs:

- patterns that worked
- reusable rules
- compact summaries
- training signals for future runs

Use DISTILL to turn one-off success into reusable knowledge.

### CONSOLIDATE

Purpose: prevent catastrophic forgetting via EWC++.

Typical outputs:

- stable memory updates
- protected important patterns
- merged learnings without overwriting prior knowledge

Use CONSOLIDATE after distillation to keep the system from losing important skills.

## Suggested Flow

1. Run the task.
2. JUDGE the result.
3. DISTILL the useful lesson.
4. CONSOLIDATE the memory.

## Common Pitfalls

1. Distilling before judging the result.
2. Consolidating weak or incorrect learnings.
3. Treating verdicts as the same thing as training signals.
4. Forgetting to preserve high-value patterns before overwriting memory.

## Verification Checklist

- [ ] Verdict produced
- [ ] Key learning extracted
- [ ] Memory consolidated safely
- [ ] Catastrophic forgetting risk reduced
