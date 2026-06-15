---
name: claude-flow-hooks
description: "Use when mapping Claude Flow hook categories to their lifecycle, context, learning, and coordination purposes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hooks, lifecycle, sessions, intelligence, learning, coordination]
    related_skills: [claude-flow-workflows, claude-flow-rolechains, swarm-advanced, hive-mind, memory-management]
---

# Claude Flow Hooks

## Overview

Use this skill as a compact reference for Claude Flow hook categories and what they are for.
It is meant for quick routing, not for deep implementation details.

## When to Use

Use when you need to:

- choose the right hook category
- understand where a hook belongs in the workflow
- map lifecycle events to session, intelligence, learning, or agent-team behavior

Do not use for:

- full workflow orchestration
- implementation of a specific hook handler
- unrelated general coding tasks

## Hook Categories

| Category | Hooks | Purpose |
|---|---|---|
| Core | pre-edit, post-edit, pre-command, post-command, pre-task, post-task | Tool lifecycle |
| Session | session-start, session-end, session-restore, notify | Context management |
| Intelligence | route, explain, pretrain, build-agents, transfer | Neural learning |
| Learning | intelligence (trajectory-start/step/end, pattern-store/search, stats, attention) | Reinforcement |
| Agent Teams | teammate-idle, task-completed | Multi-agent coordination |

## Usage Notes

- Core hooks wrap commands, edits, and tasks.
- Session hooks manage context boundaries and restore behavior.
- Intelligence hooks route work, explain choices, and support agent generation or transfer.
- Learning hooks capture trajectories, store patterns, and report stats.
- Agent team hooks help coordinate teammates around idle time and task completion.

## Common Pitfalls

1. Mixing session hooks with lifecycle hooks.
2. Using learning hooks when the task is only about command timing.
3. Treating agent-team hooks as general-purpose workflow hooks.
4. Forgetting the category determines the purpose first.

## Verification Checklist

- [ ] Category identified correctly
- [ ] Hook names matched to the right purpose
- [ ] Lifecycle vs session vs learning vs coordination separated cleanly
- [ ] Skill used as reference, not implementation
