# Live-production auth release notes

Reusable details from a React + Express + Docker Compose SaaS release where the app was switched from demo/Google-only mode to live production.

## Change pattern

- Replace demo-only auth route handlers (`410 Gone`, `GOOGLE_ONLY_AUTH`, or similar) with real service calls:
  - `POST /api/auth/register` -> validate `{ name, email, password }`, call `registerUser(...)`, return session.
  - `POST /api/auth/login` -> validate `{ email, password }`, call `loginUser(...)`, return session.
  - Keep `POST /api/auth/google` active unless explicitly removed.
- Frontend auth modal should expose email/password inputs and submit to the same API contract used by the backend.
- For production status, update health/status responses in source, e.g. map `NODE_ENV=production` to `env: "live-production"` if the product copy requires that label.
- Update visible product copy (`demo`, `VIP studio`, etc.) and docs/readme language together so tests and user-facing UI agree.

## Tests to update

- API tests should assert login/register return `200`, not old demo-only `410` responses.
- E2E route stubs must mirror the new production behavior. If the test still stubs `/api/auth/login` or `/api/auth/register` with `410`, the UI will stay on `/` even after the real backend is fixed.
- When multiple buttons share the same label (for example tab button `Login` and submit button `Login`), scope Playwright selectors:
  - Good: `page.locator('form').getByRole('button', { name: 'Login' })`
  - Avoid: `page.getByRole('button', { name: 'Login' })`
- Production smoke/live tests that reuse SQLite files should remove the temp DB before seeding to avoid false failures from duplicate users:
  - `rm -f "$DB_FILE" "$DB_FILE-wal" "$DB_FILE-shm"`

## Runtime/deploy pitfalls

- Before e2e/local smoke tests, check for an existing Docker deployment on the same backend port. A stale container can proxy old code and make tests keep receiving the old `410 Gone` response.
  - Check: `ss -ltnp '( sport = :3000 or sport = :4173 )'`
  - If needed: `docker compose down` before starting local dev/e2e servers.
- Browser tool navigation can time out against Vite/React dev servers even when the app is reachable. Fall back to Playwright from the terminal and log API responses:
  - `page.on('response', res => { if (res.url().includes('/api/')) console.log(res.status(), res.url()) })`
- After deploy, verify the public health endpoint and confirm the env label, not just that containers started:
  - `curl -fsS https://<domain>/api/health`
  - Expected shape includes `{ "ok": true, "env": "live-production" }` when the product has been switched live.

## Minimum verification sequence

1. `npm run typecheck`
2. `npm run test:unit`
3. `npm run test:api`
4. `npm run test:e2e`
5. `npm run test:live` or equivalent production smoke script
6. `bash scripts/deploy.sh`
7. `curl -fsS https://<domain>/api/health`
