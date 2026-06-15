# PHP register live-production fallback

Use this pattern for imported PHP hosts where registration must reach the live provider/API in production.

## What we learned
- Prefer the live provider config from the app database first when the container env is incomplete.
- Keep env vars as an override, but do not assume they are present in the PHP service.
- For KSR888-style register flows, `user_create` should resolve from the `api` table first (`sg_*` fields), then fall back to env reads.
- Fail closed: if the live provider does not respond, stop the registration and show a clear retry message instead of creating a local user only.
- Use short cURL timeouts for the provider call so the browser does not hang into a generic `connection lost` feel.

## Verification
- Check the live PHP container env for the provider variables; if missing, confirm the DB row instead.
- Run a container-side PHP probe against the provider endpoint and confirm whether it resolves or times out.
- Lint the PHP handlers after patching.
- Redeploy, then smoke test the live register path.

## Common pitfall
- A successful syntax check does not mean the live provider is reachable. The code can be correct while the provider endpoint still times out.
