# PHP host DB env sync and cache-busting

Use this when an imported PHP site is deployed as its own Docker service and starts returning 500s even though the database container is healthy.

## Symptom
- `mysqli_sql_exception: Access denied for user ... (using password: YES)` in the PHP app logs.
- DB container is up and the database/user exists.
- Public HTML may still render, but the page itself 500s because the PHP web container is using stale compose defaults.

## What fixed it in KSR888
1. Inspect DB container env, not just the compose file:
   - `docker exec <db-container> env | sort | grep -E '^(MARIADB|MYSQL|KSR888|DB_)'`
2. Recreate the web container with the live DB env values from the running DB container.
3. Smoke test connectivity inside the web container:
   - `docker exec <web-container> php -r 'mysqli_connect(...); echo "connect-ok\n";'`
4. Recheck the live URL after the container restart.

## Asset verification pattern
- For PHP-hosted static assets, use an exact public file URL with a cache-busting query string, for example `?v=20260509b`, when proving the fix.
- Verify the exact asset with HTTP 200/HEAD; do not rely on the browser alone because browser/CDN cache can hide a stale asset.

## Pitfalls
- Compose defaults can silently override live DB credentials during `docker compose up --force-recreate`.
- A DB container can be healthy while the web container still fails auth.
- If you inspect files with paginated `read_file` output, strip any line-number prefixes before writing them back to source; otherwise you can corrupt PHP files with stray `123|` markers.
