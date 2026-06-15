---
name: test-locally
description: "Use when running, verifying, and troubleshooting tests on the local machine before deploying or merging changes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [test, local, verification, qa, regression, build]
    related_skills: [test-driven-development, systematic-debugging, requesting-code-review]
---

# Test Locally

## Overview

Use this skill when you need to validate changes on the local machine before shipping them.

## When to Use

Use when you need to:

- run unit, integration, or smoke tests locally
- verify a build before deploy
- reproduce a bug in a local environment
- confirm a fix with a local test pass
- check for regressions after code changes

## Working Style

1. Identify the smallest relevant test scope.
2. Run the most direct local command first.
3. Inspect failures carefully before changing code.
4. Re-run the same test after each fix.
5. Finish with a broader local verification pass.

## Common Commands

- unit tests
- integration tests
- lint/typecheck
- build checks
- smoke tests
- local browser or API verification

## Common Pitfalls

- Running the whole suite before the targeted failing test.
- Assuming a pass means all paths are safe.
- Ignoring environment differences between local and deployed systems.
- Skipping the final re-run after a fix.
- Checking the wrong port or service: verify the PID/command on the port before assuming the target app is the one listening.
- Importing app code with the wrong interpreter: if system Python is missing deps, rerun with the project venv or the runtime that matches the service.

## Verification Checklist

- [ ] The relevant local test command was run
- [ ] Failures were reproduced or confirmed
- [ ] The fix was re-tested locally
- [ ] A broader verification pass was completed
