---
name: claude-consensus
description: "Use when coordinating consensus-based decisions across multiple agents, opinions, or candidate solutions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [claude, consensus, coordination, multi-agent, decision-making, voting]
    related_skills: [agent-consensus-coordinator, claude-flow-rolechains, claude-flow-workflows, reasoningbank]
---

# Claude Consensus

## Overview

Use this skill when a task requires agreement across multiple candidate solutions, agents, or viewpoints.
It helps structure disagreement, compare options, and converge on a decision.

## When to Use

Use when you need to:

- compare multiple solutions
- reconcile conflicting agent outputs
- choose a best option by vote or scoring
- summarize consensus and dissent clearly

Do not use for:

- simple single-step tasks
- work that has only one obvious answer
- direct implementation without comparison

## Consensus Process

1. Collect candidate answers or plans.
2. Identify agreement and disagreement.
3. Score options against the goal and constraints.
4. Select the best-supported direction.
5. Record the final consensus and open concerns.

## Output Shape

A useful consensus result should include:

- candidate options
- strengths and weaknesses
- tie-break criteria
- final decision
- unresolved risks

## Common Pitfalls

1. Picking the loudest option instead of the strongest one.
2. Ignoring constraints while comparing solutions.
3. Failing to record why the decision won.
4. Treating consensus as unanimity.

## Verification Checklist

- [ ] Candidate options collected
- [ ] Trade-offs compared
- [ ] Decision criteria applied
- [ ] Final consensus recorded
- [ ] Remaining risks noted
