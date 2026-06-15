---
name: building-plugins
description: "Use when designing, implementing, testing, or iterating on AI plugins that extend agent behavior with reusable logic, memory, or learning loops."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [plugins, plugin-development, agents, learning, extensibility, behavior]
    related_skills: [AgentDB Learning Plugins, AgentDB Memory Patterns, ReasoningBank Intelligence]
---

# Building Plugins

## Overview

Use this skill when creating plugins that extend agent behavior, learning, routing, or memory with reusable components.

## When to Use

Use when you need to:

- design a new agent plugin
- add reusable behavior to a workflow or model
- build learning or adaptation loops
- package agent capabilities into a modular extension
- test plugin inputs, outputs, and edge cases

## Working Style

1. Define the plugin goal and boundary.
2. Specify inputs, outputs, and state.
3. Implement the smallest useful behavior.
4. Validate with focused tests or examples.
5. Iterate until the plugin is stable and reusable.

## Good Plugin Traits

- Small and composable
- Clear contract
- Deterministic where possible
- Easy to test locally
- Safe to reuse across tasks

## Common Pitfalls

- Making plugins too broad or monolithic.
- Hiding too much state inside the plugin.
- Skipping tests for edge cases.
- Coupling plugin logic to one-off prompts or tasks.

## Verification Checklist

- [ ] Plugin purpose is clear
- [ ] Inputs and outputs are defined
- [ ] Core behavior is testable
- [ ] Reuse boundaries are respected
- [ ] Edge cases were checked
