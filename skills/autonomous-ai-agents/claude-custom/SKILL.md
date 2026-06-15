---
name: claude-custom
description: "Use when defining custom Claude Flow behaviors, integrations, or project-specific extensions that do not fit a standard core skill."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [claude, custom, extensions, integrations, project-specific]
    related_skills: [claude-core, claude-flow-ledger-executor, reasoningbank]
---

# Claude Custom

## Overview

Use this skill when a project needs custom Claude Flow behavior that is not covered by a standard skill.
It is a flexible wrapper for project-specific extensions, integrations, and special handling.

## When to Use

Use when you need to:

- define custom Claude behavior
- add project-specific integrations
- adapt core workflows to local conventions
- introduce special handling that should be reusable

Do not use for:

- tasks that already fit a narrower skill
- generic planning only
- simple one-off actions

## Usage Notes

- Keep custom behavior explicit.
- Document any project-specific assumptions.
- Prefer small extensions over broad overrides.
- Reuse core skills where possible.

## Common Pitfalls

1. Making custom behavior too broad.
2. Duplicating logic already covered by a core skill.
3. Forgetting to document project-specific assumptions.

## Verification Checklist

- [ ] Custom behavior is clearly defined
- [ ] Scope is narrow enough
- [ ] Core skills were reused where possible
- [ ] Project assumptions are documented
