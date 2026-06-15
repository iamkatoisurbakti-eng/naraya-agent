# Nusantara Claude Code Multi-Agent Roster

Use this when the user asks for Claude Code in multi-agent mode for Nusantara/ASPRI work, or says to always include `agent-self-improving`.

## Stable setup from session

Global Claude Code agents live in:

```bash
/root/.claude/agents/
```

User-level agents created for Nusantara/ASPRI:

- `nusantara-orchestrator` — decomposes work across specialists; production-aware.
- `nusantara-frontend` — mobile-first/dark premium/batik UI work.
- `nusantara-backend` — API, auth, chat history, ASPRI module routing.
- `nusantara-qa-reviewer` — build/smoke/regression and risk review.
- `nusantara-infra` — Docker/Caddy/systemd/deploy/restart implications.
- `aspri-module-manager` — ASPRI module/navigation consistency; minimal dashboard preference.
- `agent-self-improving` — workflow learning layer; proposes durable skill/memory/workflow updates after multi-agent work.

Runner script:

```bash
/root/.hermes/scripts/claude_multi_agent.sh /path/to/project "task prompt"
```

The runner should spawn at least: frontend, backend, QA, infra, and self-improving. If it is missing `agent-self-improving`, patch it before use.

## Verification

```bash
claude agents
hermes tools list | grep -E 'moa|delegation'
/root/.hermes/scripts/claude_multi_agent.sh /root/nusantara-agent/aspri-nusantara-app "test prompt"
```

If Claude Code is not authenticated, the runner should fail safely with an auth message. Do not ask the user to paste secrets in chat; ask them to run one of:

```bash
claude auth login --console
# or set ANTHROPIC_API_KEY in ~/.hermes/.env
```

## User preference embedded

For high-quality live-verified work, include the `agent-self-improving` role alongside implementation/review/deploy agents. It should not replace QA; it captures durable process improvements and prevents repeated mistakes.
