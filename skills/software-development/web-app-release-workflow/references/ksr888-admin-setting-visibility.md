# KSR888 admin setting visibility

## Session learning
- The KSR888 admin settings page should be reachable from the admin panel, not only from a developer-only middleware branch.
- The sidebar should expose a visible `Setting Website` entry for admin users.
- The `/support` admin login surface accepts either username or email and successful auth lands on `/dashboard`.

## What to check when settings are missing
1. Confirm the admin user is logged in.
2. Confirm the sidebar contains `Setting Website`.
3. Confirm `/setting` is routed inside the admin-auth branch, not inside `dev_mode`.
4. Confirm the route returns `200` after login.

## UI-only login theme note
- If the request is only to restyle login, keep the login flow untouched and apply a black/dark theme by changing background, card, input, and button colors only.
