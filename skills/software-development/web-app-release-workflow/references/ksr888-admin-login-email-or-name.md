# KSR888 admin login: email or username, level-gated

Session notes from a live KSR888 admin-login fix.

## What was learned
- The imported PHP host exposes a dedicated admin login surface at `/support` (aliased from `/admin` and `/admins`).
- The admin login handler accepts either `name` or `email` in the same field; use `filter_var($login, FILTER_VALIDATE_EMAIL)` to choose the auth credential key.
- Admin access is gated by `users.level` in `[1, 2]`.
- In this session, the production admin account already existed in `users`; setting its `level` to `1` restored admin access without changing the UI.
- Admin logins should redirect to `/dashboard` after successful auth.

## Practical verification
- Confirm the login form posts to the admin handler (`/support/login`).
- Verify the user row in the live DB has an admin level before declaring the login broken.
- Lint the modified controllers in the live PHP container, then redeploy and smoke-check the public `/support` page for the login form.

## Pitfall
- Do not force admins back to the public landing page after auth. That makes a successful login look like a failure.
- Do not assume the login identifier is username-only; on this host, email login is also valid.
