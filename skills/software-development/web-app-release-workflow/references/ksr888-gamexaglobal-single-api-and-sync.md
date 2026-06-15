# KSR888: single GameXaGlobal API source of truth

Use this note when the imported PHP host should keep only one active game API configuration.

## What was learned in this session
- The live `api` table can contain multiple provider configs, but KSR888 should treat **GameXaGlobal** as the single active game API.
- The active rows to keep are:
  - `gx_agent_code`
  - `gx_token`
  - `gx_endpoint`
  - `gx_status`
- `gx_token` is intentionally the same value as the agent code for this host's current GameXaGlobal setup.
- Legacy provider columns should be cleared/disabled to avoid ambiguous runtime behavior:
  - `sgx_*`
  - `nx_*`
  - `wsg_*`
  - `ng_*`
  - `ln_*`
- If the admin/settings UI still shows legacy provider tabs, remove the route/view entries from the actual source rather than hiding them with CSS; the goal is a clean single-provider control surface, not a visual-only patch.
- After a sync, provider images should be persisted into the DB so the homepage/categories do not need to fetch them on every request.

## Sync behavior to preserve
- During GameXaGlobal sync, store provider visuals in the database columns:
  - `provider_image`
  - `banner`
  - `mobile_banner`
- If the API omits the primary image, reuse banner/mobile banner as a fallback instead of clearing existing images.
- Clear relevant caches after sync so the homepage/category sections see the updated DB values immediately.

## Deployment reminder
- For this host, always recreate/restart the live service after deploy so the updated PHP files and DB-backed images are visible immediately.
- A successful build is not enough; the live PHP container must be restarted/recreated and then probed again.
- Verify the cleanup with both a DB query and live HTTP checks:
  - `gx_*` still populated
  - legacy provider columns empty/disabled
  - settings page shows only GameXaGlobal
  - homepage still loads cleanly after the restart
