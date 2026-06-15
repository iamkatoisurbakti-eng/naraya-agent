# Laravel admin-triggered external media sync

Session pattern from a Dockerized Laravel/PHP app (KSR888/GameXaGlobal) where production admins needed a dashboard button to refresh all game images.

## Durable workflow
1. Do not wire a dashboard button directly to an ad-hoc `tmp/` PHP script.
2. Move sync logic into an injectable Laravel service, e.g. `App\Services\...SyncService`, returning structured counts and duration.
3. Add a controller action that calls the service, catches/logs exceptions, and redirects back with a concise success/error flash message.
4. Add a POST route inside the existing admin/auth route group, with a named route and CSRF-protected Blade form/button.
5. Build/recreate the Docker service after adding source files, routes, controllers, or views.
6. Verify in the runtime container:
   - `php -l` for the new service/controller/routes/view files
   - `require "vendor/autoload.php"; class_exists(...)` for autoloaded service discovery
   - grep for the new route/button inside the container
   - unauthenticated GET should redirect if admin-protected; unauthenticated POST should 419 if CSRF-protected

## External game image sync details
- Provider-specific sweeps can be required for full coverage; broad `/api/games` alone may miss entries.
- Fetch providers first, then fetch games per provider.
- Normalize image fields defensively because providers vary key names.
- Fallback game image to provider artwork/banner if the game payload lacks its own image.
- Clear relevant catalog/provider caches after sync so the UI sees fresh images.

## Pitfalls observed
- Some Laravel bootstrap scripts failed with `Symfony\\Component\\Console\\Exception\\InvalidArgumentException: The StreamOutput class needs a stream as its first argument` when run with `docker compose exec -T`; use an app service for web-triggered work, or run CLI scripts with a PTY when necessary.
- Inline `php -r` commands are fragile under shell escaping. Prefer small temp PHP files or very carefully quoted one-liners.
- Admin route smoke tests without a logged-in session should not be treated as failures when they return expected 302/419 responses.

## Reporting
In the final report, state changed absolute paths, verification results, deployment status, and expected auth/CSRF behavior. Do not expose secrets, cookies, API keys, or connection strings.