# Brand-Safe Landing Deploy

Use this when a user asks to deploy a landing page from a local HTML file or to replace a public subdomain page.

## Guardrail
- Inspect the source HTML first.
- If the file includes third-party branding, logos, or copy that imitates another company, do not deploy it verbatim.
- Rewrite it into an original, brand-safe page before deploy.

## Minimal flow
1. Read the HTML and identify the brand/name in the title, hero, buttons, and footer.
2. Replace external branding with the user’s own brand before wiring it into routing.
3. Keep the visual mood only if it can be safely rebranded.
4. Build and deploy.
5. Verify the public HTTPS host directly, not just the local app.

## Verification
- `npm run build`
- `bash scripts/deploy.sh`
- `curl -I https://<subdomain>`
- If TLS is flaky on first deploy, restart the proxy and retry after certificate issuance.
