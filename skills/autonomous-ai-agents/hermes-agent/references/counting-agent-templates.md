# Counting Hermes Agent templates vs active agents

Use this when the user asks how many agents Hermes has.

Distinguish three meanings:

1. Active answering agent: the single current Hermes Agent process/session replying to the user.
2. Installed agent templates / agent skills: skill entries whose names start with `agent-`; these are reusable specialist templates that can be invoked/spawned for workflows.
3. App/demo agents: any agents hardcoded into a user-facing app UI. Do not answer with these unless the user explicitly asks about the app.

Commands:

```bash
# Count installed agent templates from the Hermes skill table
hermes skills list --source all | grep '│ agent-' | wc -l

# Show installed agent template rows
hermes skills list --source all | grep '│ agent-'

# Count all skills available through Hermes' skill registry/tool
# Prefer skills_list() when available; otherwise use CLI table cautiously.
```

Reporting pattern:

```text
Agent aktif yang menjawab: 1 (Hermes Agent).
Agent-template yang tersedia: <N>.
Total skills: <M>.
```

Pitfall: If a user says "bukan agent yang di app", they mean the Hermes system's own active/template agents, not the demo/UI agents in a deployed product page.