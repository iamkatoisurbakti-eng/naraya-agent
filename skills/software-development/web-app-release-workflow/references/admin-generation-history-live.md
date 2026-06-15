# Admin generation history live refresh

Use this pattern when the admin dashboard needs real-time generation history without adding a websocket service.

## Backend
- Extend `/api/dashboard/admin/summary` to include `recentGenerations` from `generation_history` joined to `users`.
- Keep the query bounded (e.g. latest 10–12 rows) and filter out expired rows with `expires_at >= CURRENT_TIMESTAMP`.
- Return only safe fields for the UI:
  - `id`
  - `capability`
  - `model`
  - `provider`
  - `prompt`
  - `costCredits`
  - `createdAt`
  - `resultJson`
  - user display fields (`name`, `email`)

## Frontend
- In the admin dashboard, poll the summary endpoint on an interval (5s is a good default) and refresh the state.
- Keep the first load loading state, then use silent refreshes so the UI does not flicker.
- Parse `resultJson` defensively in the UI; derive lightweight badges such as:
  - `kind`
  - `rawStatus`
  - `memoryHit` / cache-hit marker
- Show the credit deduction on each generation row so the log doubles as a billing audit trail.

## Pitfalls
- Do not rely on stale client state; the list must be re-fetched periodically to stay live.
- If the dashboard contains multiple sections, keep the generator history section separate from user/order cards so refreshes do not reflow the whole page.
- If the database query joins `generation_history` to `users`, make sure deleted user rows are handled gracefully (left join if needed) or the admin UI may lose historical visibility.
- If result payloads differ across providers, keep the UI tolerant of missing `rawStatus` and `kind`.
