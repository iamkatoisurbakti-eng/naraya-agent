# PHP subdomain stack deploy inside an existing Docker + Caddy repo

Use this when the user asks to deploy a provided PHP/MySQL site archive into a repo that normally serves a different app stack.

## What worked
- Treat the provided PHP app as its own source tree under a dedicated directory such as `KSR888/site`.
- Add separate Compose services for the PHP web runtime and MariaDB instead of forcing the site into the existing Node app.
- Keep the PHP site's DB connection on env vars (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) and replace any plaintext credentials found in the source.
- Seed a fresh MariaDB schema with a deterministic init SQL file under `docker-entrypoint-initdb.d/` when no DB dump is available.
- Add a dedicated Caddy site block routing the new host to the PHP container.
- After adding a brand-new hostname to Caddy, explicitly restart the `caddy` service so automatic certificate management runs for the new domain.

## Verification pattern
1. `docker compose config`
2. build the new PHP service first if the Dockerfile is new
3. `bash scripts/deploy.sh`
4. `docker compose ps`
5. `docker compose exec -T <php-service> curl -I http://127.0.0.1/`
6. `docker compose exec -T <db-service> mariadb -u... -p... -e "SHOW TABLES ..."`
7. local host-header smoke:
   - `curl -I -H 'Host: <domain>' http://127.0.0.1/`
8. if HTTPS is still failing on the public domain, inspect Caddy logs for ACME/cert issuance and restart Caddy if the hostname was just added.

## Pitfalls
- A copied site archive may include placeholder `index.html`; remove or ignore it if `index.php` is the real entrypoint.
- Dockerfile `printf` blocks are easy to break with newline quoting. Prefer simple `echo ... >> file` chains for generated config snippets.
- `docker compose up -d --remove-orphans` may leave an already-running Caddy process with old config state for a new host; a targeted `docker compose restart caddy` can be required.
- Public HTTPS `525 SSL handshake failed` after adding a hostname often means the proxy has not finished obtaining the cert yet, not that the backend PHP site is broken.
- If the original PHP app also hardcodes secondary DB/API credentials in helper scripts (`getgame.php`, `getrprovider.php`, etc.), patch those too; updating only the primary `connect.php` is incomplete.
