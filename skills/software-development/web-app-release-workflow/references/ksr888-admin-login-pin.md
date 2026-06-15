# KSR888 Admin Login + PIN Pattern

This session exposed a KSR888-specific admin login convention for imported PHP hosts.

## What changed
- Backoffice login requires three fields:
  - `username`
  - `password`
  - `pin`
- Login verification compares all three values against `tb_admin`.
- `tb_admin` needs a `pin` column in the live schema, not just in source.
- Admin bootstrap/login tests were most reliable when run from inside the container with the working directory set to the login script directory.

## Practical verification notes
- PHP file syntax checks succeeded with:
  - `php -l /var/www/html/backoffice/index.php`
  - `php -l /var/www/html/backoffice/function/cek_login.php`
  - `php -l /var/www/html/backoffice/template/page/administrator/tambah_administrator.php`
  - `php -l /var/www/html/backoffice/template/page/administrator/proses_tambah_admin.php`
- The direct container probe that confirmed credentials worked was:
  - `cd /var/www/html/backoffice/function && php -r '$_POST=["username"=>"ksr888","password"=>"ksr888","pin"=>"888888"]; include "cek_login.php"; echo json_encode($_SESSION);'`
- The live HTTPS path can be misleading because proxy/Caddy routes may redirect or return 404 for the backoffice root while the container-local script still functions.

## Pitfalls
- Don’t assume admin login is password-only on imported PHP hosts.
- If a new admin login field is added, update both:
  - the login form
  - the submit handler
  - the database schema/seed
- When adding or changing the admin seed account, keep the hash scheme aligned with the existing app conventions (`md5` in this host).

## Session-specific outcome
- Admin user `ksr888` was seeded with password `ksr888` and PIN `888888` for the backoffice login flow.
