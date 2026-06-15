---
name: nusantara-ai-saas-public-surfaces
description: Build and deploy public React app/demo surfaces in Nusantara AI SaaS, including mobile/desktop mockups, lightweight backend state, Docker release, and live verification.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [nusantara-ai-saas, react, public-route, docker, deploy, verification]
    related_skills: [web-app-release-workflow, mobile-app-builder, browser]
---

# Nusantara AI SaaS Public Surfaces

Use this skill when the user asks to create or modify a public app-like page in `/root/nusantara-ai-saas`, for example:

- mobile app UI mockups
- desktop app UI mockups
- public landing/demo routes
- small backend demo state for those surfaces
- immediate production deploy and live verification

## Standard workflow

1. Edit source, not build output.
   - React component: `web/src/components/<Name>.tsx`
   - Route registration: `web/src/main.tsx` inside `StandardRoutes`
   - Scoped styling: `web/src/styles/index.css`
   - Optional backend route: `src/routes/<feature>.ts`, mounted from `src/app.ts`

2. Keep styling scoped.
   - Add a unique root class like `.hermes-desktop-page` or `.aspri-mobile-page`.
   - Add scoped CSS overrides because the repo has global button/background rules that can flatten gradients.
   - Restore gradient classes inside the page root when needed:

```css
.page-root .bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops)) !important;
}
.page-root .bg-gradient-to-br {
  background-image: linear-gradient(to bottom right, var(--tw-gradient-stops)) !important;
}
```

3. For simple demo state, use safe JSON state.
   - Store under `data/*.json` so Docker volume persists it.
   - Never store or echo real secrets.
   - If deleting demo modules/items, sanitize persisted state as well as defaults so old entries do not reappear.

4. Build and deploy:

```bash
npm run build
docker compose up -d --build app
```

5. Verify local and live:

```bash
curl -fsS http://127.0.0.1:3001/api/health
docker compose ps app
curl --compressed -fsS http://127.0.0.1:3001/<route>
curl --compressed -fsS https://nusantara-ai.online/<route>
```

## Live verification notes

- Use `curl --compressed` for Cloudflare/live HTTPS checks; otherwise compressed responses can appear empty or fail JSON parsing.
- Browser automation may fail on this host with Chromium `ProcessSingleton` / socket directory errors. If HTTP checks, asset extraction, and container health pass, report browser as environment-blocked instead of app-failed.
- Avoid `curl ... | python3 - <<'PY'`; heredoc consumes stdin and the pipe may fail. Use a temp file, `execute_code`, or a short `node -e` parser.
- Shell safety can flag literal `&` as backgrounding. If you must check strings like `Konten & News`, construct the string in Python/Node or use `execute_code` instead of a shell pipeline.

## Reporting pattern

Keep the final answer short and Indonesian when the user expects direct deployment work:

```text
Sudah dibuat dan deploy live.
URL: https://nusantara-ai.online/<route>

Verifikasi:
- build sukses
- Docker restart sukses
- container healthy
- live HTTP OK
```

Mention changed files only when useful.