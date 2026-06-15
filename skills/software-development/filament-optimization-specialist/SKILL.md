---
name: filament-optimization-specialist
description: "Use when optimizing Laravel Filament admin panels for speed, responsiveness, query efficiency, UX smoothness, and production readiness."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [filament, laravel, optimization, performance, admin-panel, queries, ux]
    related_skills: [senior-developer, performance-analysis, test-locally, web-app-release-workflow]
---

# Filament Optimization Specialist

## Overview

Use this skill when working on Laravel Filament panels that need to feel faster, lighter, and more reliable in production.
It focuses on query efficiency, table/list performance, form responsiveness, relation loading, caching, and admin UX.

## When to Use

Use when you need to:

- speed up Filament resources, pages, widgets, or tables
- reduce slow Eloquent queries and N+1 issues
- improve form load time and action responsiveness
- optimize filters, relations, and pagination
- make admin panels more usable at scale
- prepare a Filament app for production traffic

## Working Style

1. Identify the slowest screen, query, or interaction first.
2. Measure before changing anything.
3. Remove unnecessary work from the request cycle.
4. Batch or defer expensive operations.
5. Verify the improvement with a repeatable check.

## Optimization Targets

- Table queries and sorting
- Eager loading and relation access
- Select/search options with large datasets
- Widget refresh frequency
- Form schema complexity
- Livewire re-render frequency
- Authorization checks and policy calls
- Caching of stable data

## Common Pitfalls

- Loading too many relations by default.
- Using expensive closures in hot paths.
- Rendering large tables without proper pagination or search limits.
- Recomputing the same data on every render.
- Optimizing the UI while ignoring the underlying query cost.

## Verification Checklist

- [ ] The slow path was identified
- [ ] Query or render cost was reduced
- [ ] The change was tested locally
- [ ] The UI still behaves correctly
- [ ] The improvement is measurable
