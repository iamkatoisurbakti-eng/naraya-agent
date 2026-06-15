# KSR888 game provider/game pages: remove Demo button safely

Use when the user asks that logged-in game cards show only `MAIN SEKARANG` for launching games and no `DEMO` action.

## Surfaces
- Source repo: `/root/nusantara-ai-saas/KSR888/site`
- Deploy from: `/root/nusantara-ai-saas`
- Main views that rendered Demo buttons:
  - `resources/views/slots/games.blade.php`
  - `resources/views/slots/server-b.blade.php`
- Global layout guards added for stale/injected markup:
  - `resources/views/layouts/main/master.blade.php` desktop
  - `resources/views/layouts/main/main.blade.php` mobile

## Fix pattern
1. Search all source, not just the visible page:
   ```bash
   grep -RIn "game_button_try\|game-has-try\|>DEMO<\|DEMO" resources/views KSR888/site 2>/dev/null
   ```
2. In `slots/games.blade.php` and `slots/server-b.blade.php`, remove the `<a class="btn game_button_try...">DEMO</a>` elements for both `Auth::check()` and guest branches.
3. Remove `game-has-try` from the overlay wrapper so the overlay styling is not reserved for two buttons:
   ```html
   <div class="game-overlay">
   ```
4. Add a defense-in-depth guard in both desktop and mobile main layouts in case old cache, theme JS, or injected HTML still creates a demo node:
   ```html
   <style>
     .game_button_try,
     .game-overlay .game_button_try {
       display: none !important;
       visibility: hidden !important;
       pointer-events: none !important;
     }
   </style>
   <script>
     document.addEventListener('DOMContentLoaded', function () {
       document.querySelectorAll('.game-overlay .game_button_try').forEach(function (el) {
         el.remove();
       });
     });
   </script>
   ```
5. Clear cached Blade files manually if `php artisan optimize:clear` fails in this container:
   ```bash
   docker compose exec -T ksr888-web bash -lc 'rm -f storage/framework/views/*.php bootstrap/cache/*.php || true'
   ```

## Verification
- Syntax:
  ```bash
  docker compose exec -T ksr888-web bash -lc 'php -l resources/views/slots/games.blade.php && php -l resources/views/slots/server-b.blade.php && php -l resources/views/layouts/main/master.blade.php && php -l resources/views/layouts/main/main.blade.php'
  ```
- Build/deploy/restart:
  ```bash
  docker compose build ksr888-web
  docker compose up --no-build -d ksr888-web
  docker compose restart ksr888-web
  ```
- Live smoke:
  ```bash
  curl -k -sS -L https://ksr888.online/slots -o /tmp/ksr_slots.html
  python3 - <<'PY'
  from pathlib import Path
  import re
  s = Path('/tmp/ksr_slots.html').read_text(errors='ignore')
  print('DEMO marker:', bool(re.search(r'>\s*DEMO\s*<|game_button_try|game-has-try', s, re.I)))
  print('MAIN SEKARANG:', 'MAIN SEKARANG' in s)
  PY
  ```
Expected: no visible `DEMO` marker and `MAIN SEKARANG` still present on public game pages. Provider detail pages may redirect without login; that is normal for auth-protected routes.

## Pitfalls
- Do not remove `MAIN SEKARANG` or the `/game_process/{game_code}/{game_provider}` launch path.
- Search results may miss uppercase/lowercase variants if using the file search tool; use grep inside the container/source tree as a backstop.
- `php artisan optimize:clear` can throw Symfony `StreamOutput class needs a stream as its first argument` in this container. Manual cache file removal is acceptable for Blade cache cleanup.
