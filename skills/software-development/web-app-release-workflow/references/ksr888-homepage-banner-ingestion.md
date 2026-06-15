# KSR888 homepage banner ingestion

Use when the user provides local image paths and asks to add them to the KSR888 homepage banner carousel.

## Key distinction
KSR888 has two banner mechanisms:
- Legacy desktop/mobile PHP slider fallback reads `/var/www/html/banner/*` from source `/root/nusantara-ai-saas/KSR888/banner/`.
- The main Laravel homepage (`resources/views/welcome.blade.php`) reads active rows from the `banner` database table and renders `asset('storage/' . $banner->gambar)`, so adding files only to `/banner/` may not make them appear on `/`.

## Working pattern
1. Inspect each provided image with `file`/`identify` and keep original dimensions if they already fit the carousel.
2. Copy the image into persistent public storage:
   - source: `/root/nusantara-ai-saas/KSR888/site/public/storage/post-images/<safe-name>.<ext>`
   - runtime: `/var/www/html/public/storage/post-images/<safe-name>.<ext>` (use `docker compose cp` if the container is already running).
3. Insert or update one row per image in the live DB `banner` table:
   - `gambar = 'post-images/<safe-name>.<ext>'`
   - `status = 1`
   - `nama = concise banner title`
   - `urutan = MAX(urutan)+1` unless the user specifies placement.
4. Clear Laravel caches with a PTY when non-TTY artisan fails:
   - `docker compose exec ksr888-web php artisan optimize:clear --no-ansi`
5. Restart Caddy after deploy/cache clear.

## Verification
Run live checks, not just container checks:
- Query DB rows for `gambar LIKE 'post-images/<prefix>%'` and confirm active status/order.
- `curl -k -sS -o /dev/null -w '%{http_code}' https://ksr888.online/storage/post-images/<file>?v=$(date +%s)` should return `200`.
- Fetch `https://ksr888.online/?v=$(date +%s)` with a browser-like User-Agent and grep for each new filename.
- Check `docker compose ps` and recent `ksr888-web`/`caddy` logs for fatal/parse/SQL/access-denied/type errors.

## Pitfalls
- `/banner/<file>` can return a redirect or appear reachable after following redirects while still not being part of the homepage carousel.
- The homepage will not reference `/banner/*` unless the Blade/controller path is changed; prefer the DB-backed `/storage/post-images` path for normal homepage additions.
- Rebuilding the image copies `KSR888/banner/`, but DB-backed homepage files must also exist under `site/public/storage/post-images` so they persist across rebuilds.
