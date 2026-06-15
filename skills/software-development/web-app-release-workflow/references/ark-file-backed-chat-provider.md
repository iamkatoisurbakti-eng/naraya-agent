# Ark file-backed chat provider

Use this pattern when AI Chat should authenticate from a local sensitive file such as `ark.txt` instead of a normal env var.

## What worked in this session
- A dedicated helper read the chat key from a configurable file path (`ARK_CHAT_KEY_FILE`).
- The file parser had to handle panel-style content, not just a raw single-line key.
- The chat route used a fixed model and hid the model selector in the UI.
- A direct HTTP request to the provider chat endpoint was more stable than forcing the OpenAI SDK shape to fit every Ark-style response.

## Implementation notes
- Prefer the environment variable when present; use the file only as a fallback or primary local source depending on the deployment.
- Treat the file contents as secret material: never log them, never echo them, and never store them in docs or memory.
- Keep provider status checks separate from generation calls so the UI can show availability without leaking the key.
- If the provider rejects the request with auth errors, fall back only if that is an explicit product decision.

## Verification
- Run a build after the route and UI changes.
- Run API tests that cover chat quote/status/generate paths.
- Confirm the frontend shows a single free chat path rather than a model picker.

## Pitfalls
- Do not assume the key file is a one-line raw token; inspect for `API Key:` labels or similar wrappers.
- Do not hardcode provider secrets in the repo or terminal output.
- If the provider base URL or response shape changes, prefer a small fetch wrapper over spreading SDK-specific assumptions through the route.
