# Laravel API Route Rollout

Use this reference when adding or debugging API routes in a Dockerized Laravel app.

## Pattern
1. Inspect `routes/api.php` and the target controller together.
2. Check whether global or API-only middleware is still applied:
   - `throttle:api`
   - custom middleware such as auth gates, `ApiGame`, request signing, or tenant checks
3. If the endpoint should mirror an upstream API spec, keep the route list explicit and map each contract endpoint one by one.
4. Prefer a small proxy/controller layer over putting business logic directly in route closures.
5. Run PHP lint inside the live web container, not only on the host shell.
6. Restart the web container after deploy, then verify the live URL with `curl -i`.

## Practical pitfalls seen in KSR888
- A route can be syntactically valid yet still 500 because API middleware throws before the controller runs.
- `Route::withoutMiddleware('throttle:api')` may be necessary, but it is not enough if a custom middleware still blocks the request.
- Missing Laravel runtime directories inside the container can break API requests with cache/session/view file errors. If needed, create:
  - `storage/framework/cache/data`
  - `storage/framework/sessions`
  - `storage/framework/views`
- If the proxy endpoint returns 500, inspect the stack trace for the first middleware frame before changing the controller.

## Verification
- `php -l` passes in the web container
- route file deploys into the running container
- container restarts cleanly
- `curl -i https://.../api/...` returns the expected status and JSON body
- response shape matches the upstream contract being mirrored
