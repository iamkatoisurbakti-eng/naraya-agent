# KSR888 SEO recovery notes

Session-derived notes for live crawlability recovery on the KSR888 PHP host.

## Symptom
- Root page returned HTTP 500 while robots.txt and sitemap.xml were already reachable.
- Terminal logs showed PHP fatal error from `function/connect.php`:
  - `mysqli_sql_exception: Access denied for user 'ksr888_user'@'172.18.0.4'`
- The DB container itself was healthy, but the PHP web container could not authenticate.

## Root cause pattern
- MariaDB user credentials existed, but the live password had drifted from the PHP container env/defaults.
- A `ksr888_user` account was present with multiple hosts in `mysql.global_priv` / `mysql.db`, but the authentication string did not match the password the web container used.

## Recovery sequence
1. Stop the web/db stack if needed.
2. Verify the live container env with `docker inspect` and the DB logs.
3. Confirm DB login from inside the running DB container with the exact env password.
4. If login fails, repair the DB user password in MariaDB and then recreate the web container.
5. Re-check `curl https://ksr888.online/`, `/robots.txt`, `/sitemap.xml`, `/mobile/index.php`, and `/dekstop/index.php`.

## Verification commands used
- `docker compose ps`
- `docker compose logs --tail=120 ksr888-web`
- `docker exec -i <db-container> mariadb -u<user> -p<password> -e "SELECT 1;"`
- `curl -s -D - https://ksr888.online/`
- `curl -s https://ksr888.online/ | grep -n ...`

## Important pitfall
- Do not assume the DB user password is correct just because the DB container is up.
- For live SEO work, a 500 on the homepage blocks crawlability more than missing copy does; fix the server error before tuning titles/meta.

## Added SEO improvement that was safe to ship
- Root page gained a visible crawlable landing block above the redirect script.
- The block included a keyword-rich H1 and links to mobile/desktop entry points.
- `robots.txt` and `sitemap.xml` were added for indexability.

