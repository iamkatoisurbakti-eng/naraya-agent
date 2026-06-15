# Edge/CDN 403 vs origin healthy

Use this when the public HTTPS host returns 403/1010 while the local origin/container is healthy.

Observed pattern
- `http://127.0.0.1:<port>` or the app container returns 200.
- `https://<domain>` returns 403 with a Cloudflare/edge-style body such as `error code: 1010` when requested with a default terminal user-agent.
- The same HTTPS URL returns 200 when requested with a browser-like user-agent.

What it means
- The app is usually fine; the edge/CDN is blocking the request.
- The most common culprits are Cloudflare WAF/Bot/BIC rules, Browser Integrity Check, or a security rule that dislikes non-browser clients.

Checks
1. Compare origin vs public host.
2. Retry the public host with a browser-like UA.
3. Inspect response headers/body for Cloudflare or edge fingerprints.
4. Review Cloudflare security, WAF, and bot settings before changing app code.

Remediation ideas
- Allowlist `/` and `/api/*` for legitimate traffic.
- Relax Browser Integrity Check or bot protections for the domain if they block scripts/API clients.
- Keep origin health checks separate from public-domain checks.

Pitfall
- Do not patch the app when only the edge is blocking terminal requests; the fix belongs in CDN/security settings, not source code.