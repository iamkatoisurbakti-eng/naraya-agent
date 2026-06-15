---
name: v3-document-chunking-embeddings
description: "Use when configuring document chunking, normalization, hyperbolic embeddings, and ONNX-accelerated retrieval for agentic-flow memory systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [document-chunking, normalization, embeddings, hyperbolic, poincare, onnx, retrieval]
    related_skills: [v3-retrieve-patterns, v3-ruvector-intelligence-system, memory-management]
---

# Document Chunking and Embeddings

## Overview

Use this skill when a pipeline needs document chunking, vector normalization, hyperbolic embeddings, or ONNX-accelerated similarity search.
It is a compact reference for retrieval-oriented embedding configuration.

## When to Use

Use when you need to:

- split documents into chunks with controllable size and overlap
- normalize vectors before indexing or comparison
- model hierarchical data with hyperbolic embeddings
- speed up retrieval with ONNX integration

Do not use for:

- ordinary text editing
- model training from scratch
- memory consolidation or verdict evaluation

## Core Settings

### Document Chunking

- configurable chunk size
- configurable overlap
- tune chunk boundaries for semantic continuity

### Normalization

Supported normalization modes:

- L2
- L1
- min-max
- z-score

### Hyperbolic Embeddings

Use the Poincaré ball model for hierarchical data when tree-like or nested structure matters.

### Performance

- 75x faster with agentic-flow ONNX integration
- useful for low-latency retrieval and search-heavy workloads

## Usage Notes

- Prefer smaller chunks for precise lookup and larger chunks for broader context.
- Use overlap to avoid losing context across boundaries.
- Choose normalization to match the downstream index and similarity metric.
- Use hyperbolic embeddings when the data has strong hierarchy.
- Use ONNX acceleration when retrieval latency matters.

## Common Pitfalls

1. Using too much overlap and inflating index size.
2. Choosing a normalization method that conflicts with the similarity metric.
3. Using hyperbolic embeddings for flat data that does not need them.
4. Assuming ONNX speedups without validating the deployment path.

## Verification Checklist

- [ ] Chunk size configured
- [ ] Overlap configured
- [ ] Normalization mode selected
- [ ] Hyperbolic embedding use justified
- [ ] ONNX acceleration validated
