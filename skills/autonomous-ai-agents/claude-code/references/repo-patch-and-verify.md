# Repo Patch-and-Verify Playbook

Use this when Claude Code is making real code changes in a production repo.

## Pattern
1. Read the exact target files first; if you only read a snippet, re-read the full file before overwriting it.
2. Prefer small, staged patches over a large rewrite when the file is already partially understood.
3. After each non-trivial patch set, run the narrowest useful verification first:
   - focused tests for the touched area
   - then the project build
   - then the broader API/test suite if needed
4. If a dependency/API path is unstable, try the simplest runtime path before bringing in a heavier SDK abstraction.
5. For file-based credentials, support explicit file paths and mounted locations; do not assume env vars are enough.
6. Keep all secrets redacted in output, logs, and summaries.

## Useful gotchas observed
- Partial file reads can miss nearby code that a later patch would accidentally delete.
- Build success does not guarantee the targeted test slice is green; re-run the specific suite after provider/auth changes.
- When a local credential file exists but an env key is invalid, prioritizing the file can restore expected behavior.
- If a provider SDK introduces typing/runtime friction, a direct HTTP request can be a safer first fallback.
