# KSR888 front provider click-to-games notes

Use this when a KSR888 provider card opens a provider page but the game grid is empty.

## Root cause pattern
- Front provider pages may be reading the wrong model/table.
- `BgxProvider` is not the reliable source for KSR888 front provider grids.
- The live category pages (`/slots`, `/casino`, `/sports`) should use active `SgProvider` rows from the `providers` table.

## What to verify
1. Confirm the route hits the expected controller method.
2. Confirm the controller queries `SgProvider` with `provider_status = 1`.
3. Confirm the provider type is normalized to the live code (`SL`, `SB`, `LC`, etc.).
4. Confirm the rendered `detail_url` points to `/slots/server-b/{provider_code}/{provider_type}`.
5. Confirm the running web container has the edited PHP file copied in and the container has been restarted.

## Useful live checks
- Count active provider rows by type in the web container database.
- Render the first provider and inspect its `detail_url`.
- If the page still shows nothing, check whether the runtime container is still serving stale PHP code.

## Common pitfall
- Host file edits are not enough on this deployment. Use `docker cp` into `nusantara-ai-saas-ksr888-web-1` and restart the container before validating.
