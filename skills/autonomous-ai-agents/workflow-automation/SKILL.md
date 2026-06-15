---
name: workflow-automation
description: >
  Workflow creation, execution, and template management. Automates complex multi-step processes with agent coordination.
  Use when: automating processes, creating reusable workflows, orchestrating multi-step tasks.
  Skip when: simple single-step tasks, ad-hoc operations.
---

# Workflow Automation Skill

## Purpose
Create and execute automated workflows for complex multi-step processes.

## When to Trigger
- Multi-step automated processes
- Reusable workflow creation
- Complex task orchestration
- CI/CD pipeline setup

## Commands

### Create Workflow
```bash
npx claude-flow workflow create --name "deploy-flow" --template ci
```

### Execute Workflow
```bash
npx claude-flow workflow execute --name "deploy-flow" --env production
```

### List Workflows
```bash
npx claude-flow workflow list
```

### Export Template
```bash
npx claude-flow workflow export --name "deploy-flow" --format yaml
```

### View Status
```bash
npx claude-flow workflow status --name "deploy-flow"
```

## Built-in Templates

| Template | Description |
|----------|-------------|
| `ci` | Continuous integration pipeline |
| `deploy` | Deployment workflow |
| `test` | Testing workflow |
| `release` | Release automation |
| `review` | Code review workflow |

## Workflow Structure
```yaml
name: example-workflow
steps:
  - name: analyze
    agent: researcher
    task: "Analyze requirements"
  - name: implement
    agent: coder
    depends: [analyze]
    task: "Implement solution"
  - name: test
    agent: tester
    depends: [implement]
    task: "Write and run tests"
```

## Best Practices
1. Define clear step dependencies
2. Use appropriate agent types per step
3. Include validation gates
4. Export workflows for reuse

## Applied Pattern: Scheduled maintenance jobs for Dockerized Laravel apps
Use this when a task must run on a schedule without manual clicks (for example, syncing provider/game images into DB/cache).

1. Identify the app container that has PHP/Laravel installed.
2. Create a tiny shell wrapper in `~/.hermes/scripts/` that calls `docker exec <web-container> php artisan ...`.
3. Keep the wrapper deterministic: print only aggregate status/JSON and avoid secrets.
4. Register it with `cronjob create` using the script name relative to `~/.hermes/scripts/`.
5. After creating the job, run the script once manually to validate the end-to-end path.
6. Clear or rotate relevant cache keys after successful sync so the front picks up the new DB-backed assets.

### Pitfalls
- If the host shell lacks `php`, do not troubleshoot there; execute the command inside the container.
- `cronjob create` rejects absolute script paths; use only the filename.
- If front still shows stale images, the sync may have succeeded but the cache keys were not invalidated.
- For pages that render provider/game catalogs, prefer DB-backed proxy URLs over live API image fetches.

### Reference
- See `references/ksr888-gamexaglobal-image-sync.md` for the exact runbook used in the GameXaGlobal image-sync workflow.
5. For recurring repo automation, make the action re-runnable as a standalone script first, then schedule that script.
6. When creating Hermes cron jobs, put the script under `~/.hermes/scripts/` and reference it by filename, not absolute path.
7. Verify automation by running the script once before scheduling so failures surface immediately.

## Hermes Cron Job Pattern
- Keep the scripted action deterministic and idempotent when possible.
- Store the executable logic in `~/.hermes/scripts/<name>.sh` (or another supported script type).
- Create the cron job with the script filename only; absolute or home-relative paths are rejected.
- Prefer a low-noise success payload (JSON or concise text) so scheduled runs are easy to inspect.
- If the workflow depends on the app container or services, call them explicitly inside the script and avoid manual clicking.

See `references/cronjob-scheduling.md` for a concrete example and pitfalls.
