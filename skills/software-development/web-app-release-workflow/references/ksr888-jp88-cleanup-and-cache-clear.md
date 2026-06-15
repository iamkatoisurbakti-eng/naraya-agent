# KSR888 JP88 cleanup and cache-clear notes

## What was learned
- In KSR888, public HTML can be clean while the backend still contains legacy JP88 values in the `api` table.
- `JP88` did **not** appear in the live public HTML after deploy/cache clear, but a database scan still found one hidden match in `api`.
- That hidden match was in provider config fields, not customer-facing templates.

## Useful checks
- Public HTML grep:
  - `curl -k -sS https://ksr888.online/index.php | grep -i 'JP88\|jp88'`
- Live DB scan for legacy branding:
  - query all text-like columns across all tables for `JP88` / `jp88`
- Container cache clear on imported PHP hosts:
  - `docker compose exec -T ksr888-web sh -lc 'cd /var/www/html && script -qec "php artisan optimize:clear" /dev/null'`
- Remove stale Laravel views if needed:
  - `docker compose exec -T ksr888-web sh -lc 'rm -f /var/www/html/storage/framework/views/*.php'`

## Pitfalls
- `php artisan optimize:clear` can fail in non-PTY exec with `Symfony\Component\Console\Exception\InvalidArgumentException: The StreamOutput class needs a stream as its first argument.`
- Clearing caches in the wrong context can leave old JP88 HTML in rendered views even after source files are fixed.
- A clean public grep is not enough; DB-backed provider/admin config can still carry old branding strings.

## Verification outcome pattern
- After patching, re-check:
  - public HTML on `/`, `/index.php`, `/promotion`, and any redirect aliases
  - live container cache clear succeeded
  - DB scan for legacy branding returns zero in customer-facing tables
  - any remaining match is categorized as backend/admin-only and handled separately if user asks
