---
name: devops-automator
description: "Use when automating DevOps tasks such as CI/CD, deployments, infrastructure checks, environment validation, and operational workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [devops, automation, ci-cd, deploy, infrastructure, operations, monitoring]
    related_skills: [background-tasks, workflow-automation, webhook-subscriptions, kanban-orchestrator]
---

# DevOps Automator

## Overview

Use this skill when you need to automate operational work: builds, tests, deploys, rollbacks, environment checks, and routine platform tasks.

## When to Use

Use when you need to:

- automate CI/CD pipelines
- trigger deployments or rollbacks
- validate infrastructure or environment state
- run operational checks on schedules or webhooks
- orchestrate repeatable DevOps workflows

## Working Style

1. Define the operational goal and target environment.
2. Identify the safest automation path first.
3. Add verification before and after each critical action.
4. Prefer idempotent steps.
5. Keep secrets out of logs and source.

## Common Automation Targets

- build and test pipelines
- deploy and rollback flows
- health checks and smoke tests
- webhook-triggered actions
- environment drift checks
- release coordination

## Common Pitfalls

- Automating destructive actions without verification.
- Hardcoding secrets or environment-specific values.
- Skipping post-action checks.
- Making one-off scripts instead of reusable workflows.

## Verification Checklist

- [ ] Automation goal is clear
- [ ] Safe execution order is defined
- [ ] Verification steps are included
- [ ] Secrets stay out of logs and source
- [ ] Result is reproducible or reusable
