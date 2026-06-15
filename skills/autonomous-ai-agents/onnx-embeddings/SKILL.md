---
name: onnx-embeddings
description: "Use when generating or serving embeddings with ONNX for fast, portable inference and retrieval pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [onnx, embeddings, inference, retrieval, vector-search, portability]
    related_skills: [v3-document-chunking-embeddings, v3-retrieve-patterns, sql-js-persistent-cache]
---

# ONNX Embeddings

## Overview

Use this skill when the system needs fast, portable embedding generation or embedding-based retrieval.
It focuses on ONNX inference for embeddings, with an emphasis on speed, deployment portability, and stable outputs.

## When to Use

Use when you need to:

- generate embeddings with ONNX
- deploy embedding inference without heavyweight native dependencies
- accelerate retrieval pipelines
- reuse the same embedding model across platforms

Do not use for:

- full model training
- general text generation
- tasks that do not require vector representations

## Core Concepts

- ONNX is used for portable inference.
- Embeddings should be normalized consistently with downstream similarity search.
- Keep input preprocessing stable across environments.
- Prefer batching when throughput matters.

## Suggested Workflow

1. Load the ONNX embedding model.
2. Tokenize and preprocess text consistently.
3. Run inference to produce vectors.
4. Normalize vectors if required.
5. Store or query vectors in the retrieval layer.

## Usage Notes

- Validate dimensionality before indexing.
- Match preprocessing exactly between indexing and query time.
- Batch requests for throughput when latency constraints allow it.
- Use the same model version for both cache population and retrieval.

## Common Pitfalls

1. Changing preprocessing between indexing and query time.
2. Forgetting to normalize vectors when similarity search expects it.
3. Mixing embedding dimensions from different models.
4. Assuming ONNX speedups without benchmarking the full pipeline.

## Verification Checklist

- [ ] ONNX model loads correctly
- [ ] Embedding dimension is stable
- [ ] Preprocessing is consistent
- [ ] Normalization matches retrieval requirements
- [ ] Performance was benchmarked
