# KSR888 admin login / PIN / route notes

Context
- Imported PHP host: `ksr888.online`.
- Admin panel login is served from the PHP stack, not the Node app.

What worked
- Add explicit route aliases for the admin login page when the public URL `/admin` redirects home:
  - `/admin` → admin login controller
  - `/admins` → same controller alias
  - keep `/support` as the canonical login URL if the project already uses it
- If the admin credential form includes a PIN, the backend must validate `username + password + pin` together.
- The `tb_admin` table must have a `pin` column and seed/update the login user with a matching hashed PIN.
- For the login form, make PIN required so the browser does not silently submit a partial credential set.

Verification
- `php -l` on the PHP login controller, admin route file, and admin form templates.
- `curl -I https://ksr888.online/admin`
- `curl -I https://ksr888.online/support`
- In-container functional probe by including the login handler from its working directory and asserting `$_SESSION['username']` is set after the expected POST payload.

Pitfalls
- A public `/admin` path can 200/redirect to home if the route is missing even though `/support` works.
- When running a handler directly from the CLI, include it from its own directory; relative includes like `../../function/connect.php` can fail if the CWD is wrong.
- If you add a new column to `tb_admin`, update both the schema/init SQL and any insert/update admin forms together.
- Do not assume the visible admin login page and the actual protected backoffice are the same endpoint; verify both routes.
