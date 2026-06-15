# GameXaGlobal live probe notes

Session-specific notes for testing KSR888's GameXaGlobal integration.

## What was probed
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/auth/regenerate-token`
- `GET /api/dashboard/stats`
- `GET /api/games/providers`
- `GET /api/games`
- `GET /api/players`
- `GET /api/transactions`
- `GET /api/transactions/stats`
- `GET /api/games/manage-images`
- `GET /api/games/manage-provider-images`
- `GET /api/games/upload-image`
- `GET /api/games/upload-provider-logo`
- `GET /api/players/bulk-delete`
- Bulk-upload routes discovered in the live JS bundle

## Observed behavior
- Login without valid credentials returned `400 Invalid credentials`.
- Auth-protected endpoints returned `401 Access token required` when called without a bearer token.
- Some routes unexpectedly redirected to `https://www.shodan.io`; treat those as non-API responses / misconfigured routes.
- KSR888 now has working live GameXaGlobal credentials in the runtime/DB/env path; do not print or echo them.
- Live probes from the KSR888 container returned:
  - `GET /api/auth/me` => 200 with active affiliate agent metadata.
  - `GET /api/transactions?page=1&limit=5` => 200 with `{transactions: [], pagination: ...}` when no live transactions exist.
  - `GET /api/transactions/stats` => 200 with `{stats: [], daily: [], turnover: {total_bet,total_win,turnover,bet_count,win_count,rtp_percent,net}}`.
  - `GET /api/transactions/turnover-by-player?page=1&limit=5` => 200 with `{players: [], pagination: ...}` when no player turnover exists.
- For KSR888 admin analytics, wire `/transactions-overview/search` to the overview page, not the shared `/transactions/search`, so the UI can show the correct page title and endpoint source while still using the same controller method.
- GameXaGlobal stats can expose totals under `data.turnover.total_bet` rather than `data.turnover.total_turnover`; normalize both keys.

## Useful reminders
- Enumerate endpoints from the live JS bundle before assuming the docs are complete.
- Treat credentials as redacted in notes and logs.
- When auth fails, record the exact status/body before patching client code.
- If a route redirects off-domain, do not guess its payload contract; mark it for separate investigation.
- For Laravel container verification, instantiate the controller with `Illuminate\Http\Request::create()` and inspect sanitized JSON fields (`status`, `provider`, `endpoint`, `summary`, `count`) instead of printing full secrets or raw tokens.
- If `php artisan optimize:clear` fails with Symfony `StreamOutput` in this container, run it via PTY and `script -qec 'php artisan optimize:clear --no-ansi' /dev/null`.
