# FastAPI route verification checklist

Use this when patching API routes in a live FastAPI app.

## What to verify

1. Query `/openapi.json` and confirm the new path appears.
2. Query `/health` after restart to ensure the app booted.
3. Hit the new endpoint with a real request and verify the response shape.
4. Re-run the endpoint with the same idempotent input to confirm it does not double-apply state.

## Common pitfall

When editing a partially read file, a patch can accidentally land inside the wrong block or overwrite the next decorator. If the route does not appear in OpenAPI, inspect the nearby source with a line-based read before patching again.

## Learning-state pattern

For per-user progression features:

- Store completions separately from the source content.
- Derive level from the count of unique completed material IDs per user.
- Repeated completion of the same material must not increase the level.
