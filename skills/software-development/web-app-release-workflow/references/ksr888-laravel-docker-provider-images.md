# KSR888 Laravel Docker provider-image releases

Use this reference when a KSR888 front-end change must use provider images from the `providers` table.

## Key environment facts
- Repo source: `/root/nusantara-ai-saas/KSR888/site`.
- Live service is built from `/root/nusantara-ai-saas/KSR888/docker/php/Dockerfile`, which does `COPY KSR888/site/ /var/www/html/`.
- The live `ksr888-web` container only bind-mounts `./KSR888/site/public/storage`; PHP/Blade/app source is not bind-mounted.
- Therefore editing files under `KSR888/site` is not enough for live changes. Rebuild and recreate `ksr888-web` from `/root/nusantara-ai-saas`.

## Deploy sequence
1. Edit source under `/root/nusantara-ai-saas/KSR888/site`.
2. Build: `docker compose build ksr888-web` from `/root/nusantara-ai-saas`.
3. Recreate: run `docker compose up -d --no-deps ksr888-web` as a background process if the terminal tool treats it as long-lived.
4. Wait until `curl -k -sS -o /dev/null -w '%{http_code}' https://ksr888.online/` returns `200`.
5. Clear Laravel cache after the new container is running: `docker exec nusantara-ai-saas-ksr888-web-1 sh -lc 'cd /var/www/html && php artisan optimize:clear --no-ansi && php artisan view:clear --no-ansi'`.

## Provider image implementation pattern
- Put fallback/proxy logic in `App\Models\SgProvider`, not scattered Blade expressions.
- Useful accessors:
  - `frontend_provider_image`: raw `provider_image`, fallback `mobile_banner`, fallback `banner`, fallback local icon.
  - `frontend_mobile_image`: raw `mobile_banner`, fallback `provider_image`, fallback `banner`.
  - `frontend_banner_image`: raw `banner`, fallback `provider_image`, fallback `mobile_banner`.
- For external URLs, return the app proxy route (`/game-image-proxy`) so third-party hosts do not break browser display.
- Convert hardcoded desktop nav/provider logos to DB-driven provider collections grouped by `provider_type`.
- Homepage/game rows that show provider logos should use a provider map from active DB providers, keyed by `provider_code`, so the logo next to each game is DB-driven.

## Verification
- Syntax inside rebuilt container: `php -l app/Models/SgProvider.php`, `php -l app/Providers/ViewServiceProvider.php`, `php -l app/Http/Controllers/HomeController.php`.
- Confirm the rebuilt container contains source changes with `docker exec ... grep -R 'frontend_provider_image\|providerMenus\|providerLogoFor' ...`.
- DB accessor proof with `php artisan tinker --execute` should show raw DB URL and proxied frontend URL.
- Render checks should include desktop `/`, `/slots`, `/sports`, `/casino`, `/fishing`, `/lottery`, `/cockfight`, plus mobile `/` and `/slots`.
- Count hardcoded provider-logo references in key Blade files; target `0` for `game_logos/100x70`, `game_providers_logos_sm`, and `ppslot.gif` in `navbar.blade.php`, `gamerow.blade.php`, and `gameNew.blade.php`.

## Pitfalls
- Do not trust container source after editing host files; `method_exists()`/`grep` inside container can reveal stale code if rebuild/recreate was skipped.
- `docker compose up -d ...` may be flagged by the terminal as long-lived; run it with `background=true`, then wait on the process.
- Avoid redirecting `php artisan ... >/dev/null` in this container when possible; Symfony Console may throw `The StreamOutput class needs a stream as its first argument`. Run artisan commands normally.
- `git status` may fail in `/root/nusantara-ai-saas/KSR888/site` because it is not necessarily a Git repo root.