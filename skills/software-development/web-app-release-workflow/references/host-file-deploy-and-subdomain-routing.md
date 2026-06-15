# Host-specific static landing deploy and routing

Use when a user gives a standalone HTML file to deploy as a host-specific landing page (for example `/root/KSR.html`) and expects it to appear on a dedicated subdomain.

## Pattern
1. Inspect the HTML first for branding/impersonation risk and for broken local-only asset references.
2. If the file is a fragment (for example starts with `<style>`/`<div>` and lacks `<!doctype html>`), wrap it in a complete HTML document with charset, viewport, title, description, canonical, and minimal body layout CSS.
3. Copy the file into `web/public/` so Vite serves it as a static asset. Keep a descriptive direct path (for example `/amp_ksr888_branded.html`) and add a root-domain alias only if useful.
4. Replace inaccessible upload/session asset paths (for example `/mnt/user-data/uploads/...`) with repo-served assets under `web/public/`; copy the actual logo/image into public and update the HTML to a root-relative path.
5. Add host-aware routing in `web/src/main.tsx` (or the app shell) to render the right page for that hostname.
6. If the static file must win at the root path, make sure the Express fallback does not always serve `index.html` for that host; for server-rendered/fallback apps, add an explicit host check in the Express fallback that `sendFile`s the static HTML before the generic `/` landing handler.
7. Add an explicit Caddy site block for the host (and `www` if needed) plus HTTP->HTTPS redirect entries, then validate/restart Caddy after deploy. Do not assume `{$DOMAIN}` covers unrelated domains.
8. Prefer a dedicated static path like `/KSR.html` or `/amp_ksr888_branded.html` and confirm both the root host and direct file URL return 200 after deploy.

## Pitfalls
- `express.static()` will happily serve `index.html` on the root path unless you block SPA fallback for the host or serve the file explicitly.
- If the same host already has a React app fallback, a copied HTML file in `web/public/` is not enough by itself.
- User-provided HTML may reference sandbox upload paths that do not exist in production; grep the served HTML for `/mnt/`, `/tmp/`, or local absolute paths and replace them with public assets before deploy.
- A new domain may need both app host routing and Caddy routing. A healthy app container does not prove the public domain is attached to the app.
- `docker compose restart caddy` can briefly reset local HTTP connections; retry origin/public probes after the restart instead of treating one `Recv failure` as a deployment failure.
- Verify the deployed page with `curl` against the live HTTPS host, not only the local bundle. If browser automation fails with Chromium snap/profile singleton errors, use HTTP/curl marker checks as the verification fallback.

## Verification
- `npm run build`
- `bash scripts/deploy.sh`
- `docker compose exec -T caddy caddy validate --config /etc/caddy/Caddyfile`
- `docker compose restart caddy` when the Caddyfile changed
- `curl -I https://<host>`
- `curl -I https://<host>/<file>.html`
- `curl -I https://<host>/<public-asset>` for copied images/logos
- `curl -I http://<host>` to verify HTTP redirects to HTTPS
- grep the served HTML for the expected title/copy/link markers before declaring success.
