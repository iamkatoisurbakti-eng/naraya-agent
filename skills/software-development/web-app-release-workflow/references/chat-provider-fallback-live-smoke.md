# Chat Provider Fallback and Live Smoke Test

Use this pattern when Chat AI is file-backed and one provider may fail in production, but the app should still answer.

## Scenario learned here
- Ark was the primary chat provider, reading its key from a mounted sensitive file.
- In production, Ark could fail with auth or account-balance errors (`401`, `403`, overdue balance).
- The app stayed usable by falling back to OpenAI GPT-4.1 Mini when Ark failed with provider errors.

## Recommended runtime order
1. Check chat availability via `/api/generate/status` with an authenticated request.
2. Send a minimal chat prompt through `/api/generate`.
3. If Ark returns provider/auth/balance errors, fall back only if the product decision explicitly allows it.
4. Keep the UI on one fixed free chat path; do not reintroduce a model picker just to solve provider fallback.

## Live smoke test pattern
- Verify the public host health endpoint first.
- Then test the local container endpoint (`http://127.0.0.1:3001`) before blaming the browser.
- Use a short prompt so the probe is fast and cheap.
- Confirm the JSON response includes provider, model, and text output.

## Pitfalls
- A healthy container does not prove the browser is on the new build; stale proxy or stale runtime can still serve old behavior.
- A provider-specific `401`/`403` can mean the integration path works but the upstream key/account is invalid or overdue.
- If a key is file-backed, verify the mounted file path exists in the running container and that its parser handles wrapper text such as `API Key:`.
- Never print secrets while diagnosing fallback behavior.
