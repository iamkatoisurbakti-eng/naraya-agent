# Branded Checkout Subdomain Pattern

Session note: when the user wants a checkout-style landing page for a separate brand, implement it as an original, host-aware landing page instead of cloning a third-party site.

Key steps:
1. Add a dedicated landing component under `web/src/components/` with original copy, product positioning, FAQ, and CTA.
2. Make `web/src/main.tsx` host-aware via a small `is<Host>()` helper that renders the landing page when `window.location.hostname` matches the subdomain.
3. Update `Caddyfile` so the subdomain is accepted and proxied to the app.
4. Keep the CTA/contact destinations explicit and brand-owned; do not copy another company's payment/order flow.
5. Verify with `npm run build`, `bash scripts/deploy.sh`, `docker compose ps`, and a live `curl -I` against the subdomain.

Pitfalls observed:
- Browser automation may fail in this environment with Chromium singleton/profile errors, so HTTP verification and bundle grep are the reliable fallback.
- If a public subdomain still resolves to the wrong IP, TLS can fail before the request reaches the app; confirm `dig +short A/AAAA` and the VPS public IP before blaming deploy/runtime.
- If the live host returns 200 but the browser tool fails, treat the browser failure as environment-specific unless the HTTP/bundle checks show a real regression.
