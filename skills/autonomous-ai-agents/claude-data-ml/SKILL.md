---
name: claude-data-ml
description: "Use when working on Claude Flow data and machine learning workflows such as dataset prep, model training, evaluation, retrieval, and deployment."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [claude, data, ml, machine-learning, datasets, training, evaluation, deployment]
    related_skills: [reasoningbank, v3-document-chunking-embeddings, onnx-embeddings, v3-retrieve-patterns]
---

# Claude Data / ML

## Overview

Use this skill when a task involves data processing or machine learning work in a Claude Flow-style project.
It covers dataset prep, feature or embedding pipelines, training, evaluation, retrieval, and deployment concerns.

## When to Use

Use when you need to:

- prepare or clean datasets
- design or review ML pipelines
- train, tune, or evaluate models
- build retrieval or embedding workflows
- reason about inference, latency, and deployment

Do not use for:

- plain software architecture with no ML/data component
- one-off text edits
- tasks that already fit a more specific ML or data skill

## Workflow Notes

- Start from the data source and target outcome.
- Make preprocessing explicit and reproducible.
- Keep train/validation/test boundaries clear.
- Evaluate with the right metric for the task.
- Record reusable patterns after success.

## Common Pitfalls

1. Mixing training and evaluation data.
2. Skipping preprocessing/versioning details.
3. Choosing metrics that do not match the goal.
4. Deploying without checking latency and stability.

## Verification Checklist

- [ ] Data scope is defined
- [ ] Preprocessing is reproducible
- [ ] Evaluation metric is appropriate
- [ ] Deployment/inference constraints are considered
- [ ] Useful patterns are ready to store
