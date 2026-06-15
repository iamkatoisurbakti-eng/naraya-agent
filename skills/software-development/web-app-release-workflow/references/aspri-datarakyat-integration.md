# ASPRI DATARAKYAT Integration Notes

Use this when adding or verifying the DATARAKYAT feature family inside the ASPRI FastAPI + plain HTML app.

## What the integration exposes

- Health: `GET /datarakyat/health`
- Catalog: `GET /datarakyat/catalog`
- Module list: `GET /datarakyat/modules`
- Lookup: `GET /datarakyat/check/{module}/{query}`
- Search: `GET /datarakyat/search?module=...&q=...`

## Stable behavior observed

- The backend reports the upstream civic stack metadata and active/deferred module counts.
- Active modules on this host can include: `bpom`, `lpse`, `kpu`, `bps`, `bmkg`, `simbg`.
- Search can legitimately return `count: 0` even when the module is active; verify the health/catalog response before treating it as a failure.
- Module routing should be exposed in the frontend as a dedicated ASPRI DATARAKYAT screen or card, not buried inside unrelated workflows.

## Verification order that worked

1. Hit `/datarakyat/health` and confirm the active module set.
2. Hit `/datarakyat/catalog` and confirm the module registry shape.
3. Run one direct lookup, e.g. `bpom` or `lpse`.
4. Run one search query, e.g. `lpse` + `jakarta`, and confirm the response shape even if item count is zero.
5. Restart the app only after backend/frontend edits, then re-smoke the same endpoints.

## Pitfalls

- Don’t assume a zero-result search means the integration is broken.
- Don’t add the feature only in the backend; the frontend needs a visible entry point too.
- Keep the integration lightweight and avoid coupling it to news widgets or unrelated dashboard surfaces.
- If an upstream module is deferred, surface it as deferred instead of fabricating results.
