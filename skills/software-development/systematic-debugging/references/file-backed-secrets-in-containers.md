# File-backed secrets in containers

Use this when a service should read a credential/API key from a host file but still fails in containerized or live environments.

What this session showed
- The app could read a local OpenAI key file on the host.
- The live failure came from the runtime still using an invalid env key instead of the file.
- Fixes that only change code are incomplete if the container does not mount the file.

Checklist
1. Verify the file exists on the host and inside the runtime/container.
2. Prefer an explicit override env, e.g. `OPENAI_CHAT_KEY_FILE`, so the path can differ per deployment.
3. Make file lookup precedence higher than a stale or invalid env key when the file is the intended source of truth.
4. If the service supports provider fallback, keep the file-backed provider as the first attempt and treat provider-specific failures as fallback signals.
5. Rebuild/restart the container after changing mounts or envs; cached images won’t see host file updates.

Quick probe
- Host: run a small `python3` or Node check for `exists`, `stat`, and readable size.
- Container: inspect the mounted path directly with `docker exec` or an equivalent shell into the runtime.
- If the file is present but the service still errors, check whether a higher-priority env key is shadowing it.

## Provider-first routing example

When the file is the primary auth source, treat it as the only supported path in the product flow.
- Example pattern: Ark/BytePlus-style chat reads `ark.txt` from the runtime mount and uses it as the provider key source of truth.
- Do not keep a stale OpenAI fallback in the chat route if the user explicitly wants Ark as the main provider.
- Update health/status endpoints and UI labels to name the actual provider, not a previous fallback model.
- Tests should assert both the request path and the response/provider label, not just that the chat returns text.

