# KSR888 GameXaGlobal API-only provider frontend

Use this note when the user wants the public provider catalog to show only providers that exist in GameXaGlobal.

## What changed in the session
- Front provider lists were switched to source from GameXaGlobal API responses rather than DB-only `providers` rows.
- `HomeController` now builds the homepage provider map from `gamexaglobal->providers()`.
- `SgGameController` category provider lists now filter the API provider payload directly.
- The public provider partial was simplified to render the dynamic API provider collection.
- Cache keys were versioned (`:v2`) so old provider catalogs do not linger after deployment.

## Implementation pattern
1. Fetch the provider list from the live GameXaGlobal client.
2. Normalize provider code, name, type, image, and status.
3. Filter by category/type only after the API payload is loaded.
4. Build the `providerMap` from the API collection so homepage game cards can still resolve logos.
5. Keep DB-backed provider data for admin/backoffice flows, but do not use it as the public source of truth when the request is API-only.

## Pitfalls
- If the page still shows stale providers after patching, the cache key is probably unchanged. Bump the cache key or clear app cache.
- Do not leave a DB fallback in the public front path if the user explicitly wants API-only providers.
- Preserve the public `detail_url`/launch routing contract so category cards still open the correct provider launch route.

## Verification
- Check that the rendered HTML only includes provider codes returned by GameXaGlobal.
- Confirm category pages and homepage both reflect the same provider set.
- Use cache-busted live verification after deploy, since old provider lists may be cached.