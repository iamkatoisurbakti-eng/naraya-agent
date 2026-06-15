# Host-aware subdomain live verification

Use this pattern when a web app serves a special host such as `tourguide.<domain>` or `news.<domain>` from the same codebase.

## What to verify
- The frontend router branches by `window.location.hostname` for the special host.
- The reverse proxy/Caddy config accepts the subdomain and forwards it to the same app container.
- The public HTTPS host returns 200 after deploy, even if the browser automation tool is unavailable.

## Recommended checks
1. Build and deploy the source changes first.
2. Verify the public host directly with headers:
   - `curl -s -I https://tourguide.example.com`
   - `curl -s -I https://news.example.com`
3. If the host initially returns a TLS/edge error such as 525 during certificate provisioning, wait and re-check rather than changing app code immediately.
4. If browser automation fails because Chromium cannot create a singleton/profile/socket directory, stop retrying the same launch pattern and fall back to HTTP verification.
5. For SPAs, confirm the host-specific UI by grepping the built bundle for the unique headline/CTA text when a browser DOM probe is unavailable.

## Useful pitfall
- A 200 from the origin health endpoint does not prove the special subdomain is live. Always check the subdomain itself after proxy reload/redeploy.