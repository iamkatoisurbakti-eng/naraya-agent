---
name: ai-data-remediation-engineer
description: "Use when cleaning, repairing, validating, or de-risking data used by AI systems, including datasets, labels, embeddings, retrieval corpora, and training inputs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ai, data, remediation, cleanup, validation, dataset, embeddings, quality]
    related_skills: [ai-engineer, embeddings, AgentDB Vector Search, reasoningbank, technical-writer]
---

# AI Data Remediation Engineer

## Overview

Use this skill when AI performance is affected by bad data: inconsistent labels, malformed records, duplicates, leakage, corrupted chunks, poor metadata, or retrieval corpus drift.

## When to Use

Use when you need to:

- identify and repair dataset quality issues
- remove duplicates, leakage, or malformed records
- validate labels, metadata, and schema consistency
- clean corpora used for embeddings or RAG
- patch training or evaluation data problems
- create safe remediation steps without losing useful signal

## Working Style

1. Inspect the data failure mode and its impact.
2. Classify issues by severity and recoverability.
3. Preserve original data when possible; work on copies or patches.
4. Apply targeted remediation, not blanket destruction.
5. Re-validate after cleaning.

## Common Data Problems

- Duplicate or near-duplicate records
- Bad or missing labels
- Schema drift
- Leakage between train/test/eval sets
- Broken timestamps or identifiers
- Malformed text chunks or embeddings metadata
- Stale documents in retrieval indexes

## Common Pitfalls

- Over-cleaning and deleting useful edge cases.
- Fixing symptoms without tracing the source.
- Failing to preserve provenance.
- Mixing remediation with model changes.
- Skipping revalidation after cleanup.

## Verification Checklist

- [ ] The data issue was identified clearly
- [ ] Remediation preserved useful signal
- [ ] Provenance or backups were retained
- [ ] The cleaned data was revalidated
- [ ] Downstream impact was checked
