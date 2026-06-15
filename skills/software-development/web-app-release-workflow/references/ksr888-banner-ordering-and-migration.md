# KSR888 Banner Ordering and Migration

Use this note when a host-specific PHP app needs banner ordering without changing the visible design.

## Pattern
- Add an integer `urutan` column to the banner table.
- In admin create/edit forms, expose `urutan` as an optional numeric field.
- In admin listing, sort with `orderBy('urutan')->orderByDesc('id')` so explicit order wins and newer items stay stable as a tie-breaker.
- In the public/home controller, use the same order clause for only-active banners.
- Backfill old rows on migration so existing banners keep a predictable order instead of all defaulting to zero.

## Practical implementation
1. Create a migration that adds `urutan` with a default of `0`.
2. In the migration `up()`, update existing rows after the schema change:
   - fetch banners in descending `id`
   - assign `urutan = 1, 2, 3...`
3. Update the banner controller:
   - `index()` uses ordered query
   - `store()` saves `urutan ?? (Banner::max('urutan') + 1)`
   - `update()` preserves or updates `urutan`
4. Update the admin banner Blade view:
   - add an `Urutan` input to add/edit modals
   - add an `Urutan` column to the table
5. Deploy, then run the migration directly with the specific path if the host already has other unrelated migrations that would fail.

## Verification
- Check syntax for the controller and view files.
- Run the migration with the exact path when a full `migrate --force` is blocked by old tables.
- Confirm the live DB has the new column and that rows show the intended order.
- Confirm the public page still renders the same layout, only the order changes.

## Pitfalls
- On this host, plain `docker compose exec ... php artisan migrate --force` can fail for unrelated legacy migrations (for example an already-existing table).
- Use `php artisan migrate --force --path=database/migrations/<file>.php` to apply only the banner-order migration.
- If the app is served from a PHP container, verify the migration path inside `/var/www/html/database/migrations/...`.
- `php artisan` may require a PTY wrapper or container shell context on this host; avoid assuming a non-PTY exec will work for console commands.
- Do not change banner visuals to fake the order; the ordering must come from data, not CSS.