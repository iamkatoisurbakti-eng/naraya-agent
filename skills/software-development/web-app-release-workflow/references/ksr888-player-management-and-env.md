# KSR888 Player Management + GameXaGlobal env notes

Session learnings for Dockerized KSR888 Laravel app at `/root/nusantara-ai-saas/KSR888/site`.

## Player Management implementation pattern

When adding admin-facing GameXaGlobal player controls:

- Reuse the existing GameXaGlobal helper: `App\Http\Api\gamexaglobal`.
- Admin routes live inside the authenticated admin group in `routes/web.php`.
- A safe controller home is `App\Http\Controllers\backoffice\DatamemberController` because it already owns member/admin data views.
- Add a class-level page instead of only extending DataTables:
  - route: `GET /players` named `players.management`
  - view: `resources/views/admin/players/management.blade.php`
  - sidebar link under Member / Member Management
- Useful actions:
  - list local users with `User::with('Saldo')`
  - fetch provider players with `$gx->players(['search'=>..., 'page'=>1, 'limit'=>...])`
  - normalize provider player keys: `id|player_id|user_id`, `username|user_code|player|name`, `balance|wallet.balance`
  - sync local balance with `$gx->playerBalance($providerPlayerId)` and `Saldo::updateOrCreate(...)`
  - create missing provider players with `$gx->createPlayer(...)`

## Deployment / verification

- Rebuild and recreate after source changes:
  - `docker compose build ksr888-web`
  - `docker compose up -d --force-recreate ksr888-web`
- In this environment, foreground `docker compose up -d ...` may be flagged as long-running; run it with background mode if using Hermes terminal tools.
- `php artisan optimize:clear` can fail in this container with Symfony Console stream errors. Use the app's `/clear-cache` route instead when available.
- Syntax checks must run inside the container:
  - `docker exec nusantara-ai-saas-ksr888-web-1 php -l app/Http/Controllers/backoffice/DatamemberController.php`
  - `docker exec nusantara-ai-saas-ksr888-web-1 php -l routes/web.php`
  - `docker exec nusantara-ai-saas-ksr888-web-1 php -l resources/views/admin/players/management.blade.php`
- `/players` redirects when unauthenticated; a 302 to `/` is expected from curl without an admin session.
- To verify route/view without browser login, bootstrap Laravel from `php -r` inside the container, seed a request instance before kernel bootstrap, login an admin with `Auth::loginUsingId(...)`, call the controller method, and assert rendered content contains `Player Management` and `GameXaGlobal`.

## Env update pattern

For GameXaGlobal agent code updates in KSR888, set `GAME_LIBRARY_AGENT_CODE` in both:

- `/root/nusantara-ai-saas/.env` — Docker Compose source for the running container
- `/root/nusantara-ai-saas/KSR888/site/.env` — Laravel app-local env/source copy

Then recreate `ksr888-web` so Compose injects the changed env. Verify without echoing secrets unnecessarily:

- `docker exec nusantara-ai-saas-ksr888-web-1 php -r 'echo getenv("GAME_LIBRARY_AGENT_CODE") === "EXPECTED" ? "container_agent_code_ok=1\n" : "container_agent_code_ok=0\n";'`

Keep tokens/passwords redacted; agent codes may be operational identifiers, so avoid overexposing them in summaries beyond confirming the key was set.