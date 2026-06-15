# Subdomain DNS Pointing and TLS Smoke

Session note: a live subdomain can look broken even when the app and deploy are fine if DNS still points to another origin.

Observed pattern:
- `dig +short A <subdomain>` returned an IP that was not the current VPS.
- `curl -vkI https://<subdomain>` failed with a TLS internal error before the request reached the app.
- Caddy logs later showed ACME/http-01 traffic and certificate issuance on the correct server, which confirmed the local stack was healthy.

Verification sequence:
1. Check the public DNS first:
   - `dig +short A <subdomain>`
   - `dig +short AAAA <subdomain>`
2. Compare those answers with the actual VPS/public egress IP.
3. If the subdomain points elsewhere, fix DNS/Cloudflare before changing app code.
4. Re-run `curl -I https://<subdomain>` after DNS propagates.
5. Only then diagnose app/runtime issues.

Useful commands:
- `curl -s https://ifconfig.me` to confirm the current machine's public IP from the terminal.
- `docker logs <caddy-container> --tail 100` to see whether TLS issuance is happening on the intended host.

Pitfall:
- A failed browser smoke or TLS handshake is not always an app bug; verify DNS placement first when the public hostname is brand new or recently repointed.
