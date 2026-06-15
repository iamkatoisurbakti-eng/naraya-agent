---
name: ai-engineer
description: "Use when building AI-powered products, workflows, or agents across prompting, RAG, evaluation, tooling, and deployment."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ai-engineer, llm, rag, evaluation, prompting, agents, deployment]
    related_skills: [embeddings, reasoningbank, AgentDB Vector Search, claude-analysis, building-plugins]
---

# AI Engineer

## Overview

Use this skill for end-to-end AI product work: designing prompts, retrieval, tool use, evaluations, memory, and production readiness.

## When to Use

Use when you need to:

- design or improve an AI feature
- build RAG or semantic retrieval flows
- choose models, prompts, tools, or routing logic
- add evaluation, guardrails, or feedback loops
- deploy or iterate on AI-assisted workflows

## Working Style

1. Define the user goal and failure modes.
2. Choose the smallest AI architecture that works.
3. Add retrieval, tools, or memory only where needed.
4. Measure quality with tests or evals.
5. Harden for latency, safety, and cost.

## Core Concerns

- Prompt quality and structure
- Retrieval accuracy and context control
- Tool selection and orchestration
- Evaluation, regression, and red-team checks
- Cost, latency, and reliability
- Privacy, secrets, and safety boundaries

## Common Pitfalls

- Overcomplicated architecture too early.
- Shipping without evals.
- Relying on prompts alone when retrieval or tools are needed.
- Ignoring token cost, latency, or failure recovery.

## Verification Checklist

- [ ] Goal and failure modes are defined
- [ ] Model/prompt/tool approach is justified
- [ ] Retrieval or memory is scoped appropriately
- [ ] Eval or test coverage exists
- [ ] Safety and cost were reviewed
