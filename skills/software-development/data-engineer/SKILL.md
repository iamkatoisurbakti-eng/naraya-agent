---
name: data-engineer
description: "Use when building, maintaining, or optimizing data pipelines, ETL/ELT flows, schemas, warehousing, and production data infrastructure."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [data-engineering, pipelines, etl, elt, warehouse, schema, orchestration]
    related_skills: [software-architect, senior-developer, technical-writer, test-locally]
---

# Data Engineer

## Overview

Use this skill when working on data infrastructure: ingesting, transforming, validating, storing, and serving data reliably.

## When to Use

Use when you need to:

- build or improve data pipelines
- design ETL or ELT flows
- manage schemas and warehouse tables
- reduce data latency or cost
- validate data quality and freshness
- prepare data for analytics or downstream AI use

## Working Style

1. Identify data sources, sinks, and SLAs.
2. Define the data model and transformation steps.
3. Add validation and observability early.
4. Optimize for reliability before cleverness.
5. Verify freshness, completeness, and correctness.

## Core Concerns

- Ingestion reliability
- Schema evolution
- Batch vs streaming trade-offs
- Data quality checks
- Orchestration and retries
- Lineage and observability
- Warehouse performance and cost

## Common Pitfalls

- Building pipelines without validation.
- Ignoring schema drift.
- Making transformations opaque or hard to audit.
- Overcomplicating orchestration.
- Skipping freshness and completeness checks.

## Verification Checklist

- [ ] Sources and sinks are clear
- [ ] Transformations are documented
- [ ] Data quality checks exist
- [ ] Observability is in place
- [ ] Pipeline behavior was verified
