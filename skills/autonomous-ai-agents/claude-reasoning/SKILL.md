---
name: claude-reasoning
description: "Use when applying structured reasoning for problem solving, decision making, chain-of-thought style analysis, and evaluating alternatives."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [claude, reasoning, analysis, decisions, alternatives, structured-thinking]
    related_skills: [claude-consensus, claude-analysis, reasoningbank, claude-core]
---

# Claude Reasoning

## Overview

Use this skill when a task needs structured reasoning instead of direct execution.
It helps break down the problem, compare alternatives, and make a defensible decision.

## When to Use

Use when you need to:

- analyze a complex problem
- compare multiple approaches
- explain a decision clearly
- reason through trade-offs and constraints
- identify assumptions and unknowns

Do not use for:

- trivial one-step tasks
- direct code execution or file edits
- tasks that already have a clear single action

## Reasoning Flow

1. Define the goal.
2. List constraints and known facts.
3. Break the problem into parts.
4. Compare candidate approaches.
5. Choose the strongest option.
6. State assumptions and risks.

## Output Shape

A strong reasoning result should include:

- problem summary
- facts and constraints
- options considered
- trade-offs
- final conclusion
- remaining uncertainty

## Common Pitfalls

1. Jumping to a conclusion too early.
2. Forgetting key constraints.
3. Treating a guess as a fact.
4. Not separating evidence from interpretation.

## Verification Checklist

- [ ] Goal is clear
- [ ] Constraints are listed
- [ ] Options are compared
- [ ] Decision is justified
- [ ] Risks or uncertainty are noted
