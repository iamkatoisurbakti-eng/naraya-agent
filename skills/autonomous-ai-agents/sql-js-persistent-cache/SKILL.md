---
name: sql-js-persistent-cache
description: "Use when implementing a cross-platform persistent cache with sql.js/WASM SQLite and no native compilation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sqlite, sql.js, wasm, cache, persistence, cross-platform, no-native-build]
    related_skills: [v3-retrieve-patterns, v3-document-chunking-embeddings, v3-neural-substrate-ruvector]
---

# sql.js Persistent Cache

## Overview

Use this skill when you need a persistent cache that works across platforms without native compilation.
It is designed around sql.js, SQLite in WASM, and a simple persistence layer for cache data.

## When to Use

Use when you need to:

- store cache entries in SQLite
- run on platforms where native compilation is undesirable
- use WASM-based storage for portability
- keep cache behavior consistent across environments

Do not use for:

- high-write transactional databases
- server-only databases that can rely on native SQLite extensions
- cases where a remote database is already the right choice

## Core Ideas

- sql.js provides SQLite compiled to WebAssembly.
- Persistent cache data should be saved and restored explicitly.
- Keep the schema small and the cache keys deterministic.
- Prefer portable serialization for values.

## Suggested Pattern

1. Initialize the WASM SQLite database.
2. Create a cache table with key, value, and updated_at fields.
3. Load persisted cache state on startup.
4. Write back cache changes periodically or on shutdown.
5. Evict stale entries with a simple policy.

## Example Schema

```sql
CREATE TABLE IF NOT EXISTS cache_entries (
  cache_key TEXT PRIMARY KEY,
  cache_value TEXT NOT NULL,
  updated_at INTEGER NOT NULL
);
```

## Usage Notes

- Use stable cache keys.
- Serialize values as JSON unless a different format is required.
- Keep persistence writes batched when possible.
- Validate restore logic on every platform you support.

## Common Pitfalls

1. Assuming WASM storage is automatically persistent.
2. Using large binary blobs without a clear serialization plan.
3. Forgetting to export the database state after mutation.
4. Treating this like a full relational backend instead of a cache.

## Verification Checklist

- [ ] sql.js initialized correctly
- [ ] Cache table created
- [ ] Persistence load/save path works
- [ ] Cache keys are stable
- [ ] No native compilation is required
