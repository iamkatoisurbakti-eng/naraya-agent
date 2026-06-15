# KSR888 Game Library / Agent Balance Panel

Context:
- Imported PHP host: `ksr888.online`
- Admin panel card previously labeled `Agent Balance NX`
- Live source of truth now comes from `GameXaGlobal`

Pattern:
1. Keep the visible admin label aligned with the active provider, e.g. `Agent Balance - GameXaGlobal`.
2. Remove stale secondary provider cards before wiring the live source: delete `Agent Balance BGX`, `balance2`, `/get-balance2`, `agentbalance2()`, and any `ksr888:bgx-agentbalance2` cache usage so admins see one source of truth.
3. Use the direct GameXaGlobal API wrapper in the controller instead of a legacy provider helper when the old API is no longer active.
4. Make `/get-balance` return a live response shape, not only a bare number:
   - `status`
   - `provider: GameXaGlobal`
   - `realtime: true`
   - `balance`
   - `agent_status`
   - `server_time`
5. Add no-store headers on `/get-balance`:
   - `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`
   - `Pragma: no-cache`
6. On the front-end fetch, use `cache: 'no-store'`, `credentials: 'same-origin'`, an `Accept: application/json` header, and a timestamp query such as `/get-balance?_=${Date.now()}` so the admin panel does not show stale balance values after deploy.
7. Poll the dashboard card every ~10 seconds and show a compact status line such as `Live GameXaGlobal • active • <server_time>`.
8. After deploy, restart/recreate the host-specific PHP container so the new label and live API path show immediately.

Verification:
- Directly probe GameXaGlobal `/api/auth/me` with masked token output and confirm `status=200`, `agent.balance`, and `agent.status`.
- Verify the protected public route behavior: unauthenticated `/get-balance` may return `302`, while removed `/get-balance2` should return `404`.
- Grep the deployed container for `Live GameXaGlobal`, `/get-balance?_=`, and absence of `Agent Balance BGX`, `balance2`, `get-balance2`, `agentbalance2`.

Pitfall:
- A cached balance endpoint can make the panel look broken even when the API call is healthy.
- If the balance API returns a nested payload, probe common shapes (`agent.balance`, `balance`, `data.agent.balance`, `data.balance`) before falling back to `0`.
- `php artisan optimize:clear` may fail without a real TTY in this stack; retry with `docker compose exec ksr888-web script -qec 'php artisan optimize:clear --no-ansi' /dev/null` or a PTY exec.
