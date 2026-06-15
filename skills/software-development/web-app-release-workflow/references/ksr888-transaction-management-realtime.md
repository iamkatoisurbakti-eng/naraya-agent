---
name: ksr888-transaction-management-realtime
summary: KSR888 Transaction Management real-time GameXaGlobal polling pattern and verification notes.
---

# KSR888 Transaction Management real-time API notes

Use when the admin Transaction Management page needs live GameXaGlobal transaction/stat/turnover data, or when the user asks to set the API to real-time.

## Pattern
- Keep `/transactions-overview` admin-protected and backed by `GameSettingController::getGameHistory`.
- Use GameXaGlobal endpoints via the existing helper:
  - `/api/transactions` for all-player Transaction Management rows.
  - `/api/transactions/stats` for summary cards.
  - `/api/transactions/turnover-by-player` for turnover table.
  - `/api/players/{playerId}/transactions` for per-player history.
- For all-player mode, send a sentinel value such as `__all__` from the UI and route it to `$gx->transactions(...)` instead of requiring a selected player.
- Return `realtime: true`, `server_time`, and no-cache headers from the JSON route:
  - `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`
  - `Pragma: no-cache`
- In the Blade UI, add polling controls rather than WebSockets for this PHP host:
  - status badge (`Real-time aktif/sinkron/error`)
  - last-updated timestamp
  - interval selector (5/10/30 seconds)
  - ON/OFF toggle
  - `setInterval(() => loadAnalytics(true), interval)` with a `loading` guard so polling cannot overlap.
- Silent polling should not pop SweetAlert on every failure; reserve modal errors for manual searches.

## Verification
After rebuild/recreate and Caddy restart:

```bash
curl -k -L -sS -A "$UA" https://ksr888.online/clear-cache

docker compose exec -T ksr888-web php -l /var/www/html/app/Http/Controllers/backoffice/GameSettingController.php
docker compose exec -T ksr888-web php -l /var/www/html/resources/views/admin/history_play/history.blade.php

docker compose exec -T ksr888-web sh -lc "grep -R \"Real-time ON\|refreshInterval\|setInterval\|server_time\|Cache-Control\|no-store\" -n /var/www/html/resources/views/admin/history_play/history.blade.php /var/www/html/app/Http/Controllers/backoffice/GameSettingController.php"
```

Masked direct provider smoke, without printing credentials:
- DB connection ok.
- GameXa config present.
- `/api/auth/me` returns 200.
- `/api/transactions`, `/api/transactions/stats`, and `/api/transactions/turnover-by-player` return 200.

## Pitfalls
- `/transactions-overview` may return the login/home shell when not authenticated; do not treat lack of visible Transaction Management copy in a public curl as proof the admin page failed. Verify container source grep plus authenticated/browser check when credentials are available.
- Do not print GameXa token/agent values during smoke probes.
- `php artisan` can fail with Symfony `StreamOutput` on this imported PHP host; use direct `php -l`, HTTP probes, and small temporary PHP/cURL probes instead, then delete temporary files.
