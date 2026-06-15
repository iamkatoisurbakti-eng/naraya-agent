# KSR888 admin balance card decommission

Use when removing a legacy provider balance card from the KSR888 admin dashboard while keeping the active GameXaGlobal balance card.

## Pattern
1. Search source and runtime for all user-facing and JS/backend hooks:
   - `Agent Balance BGX`
   - `balance2`
   - `/get-balance2`
   - `agentbalance2`
   - legacy cache keys such as `ksr888:bgx-agentbalance2`
2. Remove the card markup from `resources/views/admin/backoffice.blade.php`.
3. Remove the matching fetch script so the browser does not call a deleted endpoint.
4. Remove the route from `routes/web.php`.
5. Remove the controller method and unused imports from `app/Http/Controllers/backoffice/BackofficeController.php`.
6. Keep the active GameXaGlobal balance card and `/get-balance` route intact.
7. Rebuild/recreate `ksr888-web`, clear cache, restart Caddy.

## Verification
- PHP lint the changed files before deploy.
- Grep source and running container for stale strings:
  - `Agent Balance BGX|balance2|get-balance2|agentbalance2|ksr888:bgx-agentbalance2`
- Live checks:
  - `/support` returns `200`
  - `/dashboard` redirects/protects with auth when unauthenticated
  - `/get-balance` remains auth-protected
  - `/get-balance2` returns `404`
- Check recent logs for fatal/parse/syntax/SQL/access denied/type errors.

## Pitfalls
- Removing only the visible card leaves a noisy background fetch to `/get-balance2`.
- Removing only the route leaves dead code/imports that can confuse future provider cleanup.
- Do not remove `/get-balance`; it is the active GameXaGlobal balance path.
