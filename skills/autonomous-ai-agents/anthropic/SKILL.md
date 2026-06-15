---
name: anthropic
description: "Use when working with Anthropic-specific models, APIs, prompting patterns, and integration behavior in Claude-based workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [anthropic, claude, api, prompting, integration, models]
    related_skills: [claude-core, claude-analysis, claude-reasoning, architecture-system-design]
---

# Anthropic

## Overview

Use this skill when a task involves Anthropic-specific model behavior, API usage, prompting patterns, or integration details.
It is a compact reference for working with Claude-style systems.

## When to Use

Use when you need to:

- write or review Anthropic prompts
- integrate with Anthropic APIs
- reason about Claude model behavior
- adapt workflows for Anthropic-specific constraints

Do not use for:

- generic model-agnostic tasks
- unrelated infrastructure work
- tasks that already fit a narrower skill

## Usage Notes

- Keep prompts explicit and structured.
- Match the output format to the downstream consumer.
- Prefer small, verifiable changes to prompting or API calls.
- Document any Anthropic-specific assumptions.

## Common Pitfalls

1. Assuming all Claude models behave identically.
2. Ignoring prompt structure and role separation.
3. Mixing Anthropic-specific details into unrelated workflows.

## Verification Checklist

- [ ] Anthropic-specific need is clear
- [ ] Prompt or API behavior is documented
- [ ] Output format is compatible
- [ ] Any constraints are noted
