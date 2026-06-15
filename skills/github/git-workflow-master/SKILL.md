---
name: git-workflow-master
description: "Use when managing the full Git workflow: branching, commits, rebases, merges, conflict resolution, history hygiene, and release-safe collaboration."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [git, workflow, branching, commits, rebase, merge, conflicts, collaboration]
    related_skills: [github-pr-workflow, github-repo-management, github-auth, senior-developer]
---

# Git Workflow Master

## Overview

Use this skill when the task is about working expertly with Git itself: branch hygiene, commit strategy, rebasing, merging, conflict resolution, and clean repository history.

## When to Use

Use when you need to:

- create and manage feature branches
- write or clean up commit history
- rebase or merge safely
- resolve conflicts confidently
- prepare branches for review or release
- keep history understandable and minimal

## Working Style

1. Start from a known clean state.
2. Keep branches focused and short-lived.
3. Use descriptive commit messages.
4. Prefer rebase for local cleanup, merge when preserving context matters.
5. Verify state before and after history operations.

## Core Concerns

- Branch naming and lifecycle
- Commit granularity and message quality
- Rebase vs merge trade-offs
- Conflict resolution and reviewability
- Remote tracking and push safety
- History rewriting risk

## Common Pitfalls

- Rewriting shared history without coordination.
- Mixing unrelated changes in one branch.
- Losing track of remote branch state.
- Resolving conflicts mechanically without understanding them.
- Forgetting to verify the final branch status.

## Verification Checklist

- [ ] Branch state is known
- [ ] History changes are intentional
- [ ] Conflicts were resolved correctly
- [ ] Remote tracking is correct
- [ ] Final git status is clean
