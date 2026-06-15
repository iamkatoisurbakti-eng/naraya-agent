# Resuming After Context Compaction

Use this checklist when a session resumes after a large context drop, partial transcript, or uncertain handoff.

## Goals

- Recover current repo state quickly.
- Verify what was actually changed on disk before trusting prior claims.
- Continue from the present state, not the remembered storyline.

## Recommended order

1. Inspect the repo root and active branch/state.
2. Read the most relevant files directly from disk.
3. Check recent diffs/logs if available.
4. Reconstruct the active task from current code and any stable memory.
5. Verify claimed work with live checks before continuing.

## Pitfalls

- Trusting a compacted summary without checking files.
- Assuming prior assistant output reflects reality.
- Repeating work that already exists on disk.
- Treating memory as a source of truth for transient session state.

## Practical rule

If the task sounds like “continue where we left off,” verify the actual repository state first, then choose the next change from what exists on disk.