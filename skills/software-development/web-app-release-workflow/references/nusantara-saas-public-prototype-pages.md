# Nusantara AI SaaS public prototype pages

Use when the user asks to create/deploy a public design prototype page inside `/root/nusantara-ai-saas` (for example mobile app mockups, desktop app mockups, Hermes/ASPRI previews).

## Proven workflow

1. Add a dedicated React component under:
   - `web/src/components/<FeaturePage>.tsx`
2. Register public routes in:
   - `web/src/main.tsx`
   - keep aliases when useful, e.g. `/hermes-desktop` and `/hermes-agent-desktop`.
3. Add scoped CSS in:
   - `web/src/styles/index.css`
   - use a page root class (e.g. `.hermes-desktop-page`) to override the repo's global button/background rules without changing unrelated pages.
4. Build locally before deploy:
   - `npm run build`
5. Deploy/restart live app:
   - `docker compose up -d --build app`
   - wait for completion, then check `docker compose ps app`.
6. Verify:
   - `curl -fsS http://127.0.0.1:3001/api/health`
   - `curl --compressed -fsS http://127.0.0.1:3001/<route>` and ensure an asset script exists.
   - `curl --compressed -fsS https://nusantara-ai.online/<route>` and ensure the live HTML references the new asset.

## Pitfalls

- The global CSS in this repo has broad `:where(button...)` and dashboard background overrides. For highly styled prototype pages, add page-scoped CSS restores such as `.my-page .bg-gradient-to-r { background-image: linear-gradient(...) !important; }` and explicit `.text-black/.bg-white` overrides as needed.
- Browser automation may fail on this host with Chromium ProcessSingleton/socket profile errors. Do not keep retrying the same browser call; use HTTP/asset verification and report browser as environment-blocked if the app checks pass.
- Prefer source edits, not `web/dist`; Docker rebuild copies fresh `web/dist` from the builder stage.
- Keep secrets out of UI copy and final reports.
