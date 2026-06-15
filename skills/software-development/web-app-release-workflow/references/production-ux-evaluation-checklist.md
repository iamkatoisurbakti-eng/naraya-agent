# Production UX Evaluation Checklist

Use when the user asks to evaluate a live web app (for example `nusantara-ai.online`) rather than immediately modify it.

## Guardrail
- Treat “evaluasi/evaluate/review” as an audit/report request unless the user explicitly asks to update/deploy.
- Do not leave partial source edits in progress during an evaluation. If edits were already started from a previous request, mention them separately and do not deploy them as part of the audit.

## Live checks
1. HTTP and API health:
   - `curl -I -L https://<host>`
   - `curl -fsS https://<host>/api/health`
   - `curl -fsS https://<host>/api/version`
2. Container/runtime status when local production access exists:
   - `docker compose ps`
3. Browser smoke with mobile and desktop viewports:
   - Check page title, first H1, visible button labels, console/page errors, horizontal overflow, DOM/media counts, and a short body-text sample.
   - If Playwright bundled Chromium is missing, launch with installed Chromium: `chromium.launch({ executablePath: '/snap/bin/chromium', args: ['--no-sandbox'] })`.
4. Build/type safety:
   - `npm run build:web`
   - `npm run typecheck`

## UX findings to look for
- CTA text duplication from responsive spans (for example screen text like `UpgradeUpgrade Subscription`); fix with conditional rendering or `aria-hidden`/accessible labels.
- Landing pages that are too long on mobile; report `scrollHeight` vs viewport height and recommend a shorter hierarchy.
- Too many videos/media on the homepage; count `video` elements and inspect duplicated static assets.
- Public news/landing surfaces should preserve Nusantara-AI News branding and avoid visible third-party source labels when that is the product convention.
- Prompt-first/product-first studio flows should hide model, ratio, duration, quality, and upload controls behind `Pengaturan lanjut` unless the user asks for expert mode.

## Production hygiene checks
- `index.html` should not be served with `Cache-Control: public, max-age=31536000, immutable`; reserve immutable caching for hashed JS/CSS/media assets.
- Public pricing endpoints/UI should not expose internal billing fields; if `/api/payments/plans` is auth-only, note whether landing pricing is hardcoded or needs a safe public plan endpoint.
- If the production directory is not a git repository, flag rollback/audit risk and recommend git-tracked deploys or release tags.
- Check `du -sh web/dist web/public data` and top static files to find media bloat and generated-data growth.

## Report shape
- Start with overall status and score.
- List verified evidence (HTTP status, health, build/typecheck, container state, browser smoke).
- Separate P0/P1/P2 priorities.
- Keep secrets out of the report; never echo env values or API keys.
