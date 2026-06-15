# Google Sign-In GIS + Supabase Env Release Notes

Context: Nusantara AI SaaS, Dockerized React/Vite + Express app. Session fixed Google Sign-In failing around `https://accounts.google.com/gsi/transform` and added Supabase agent skills/env passthrough.

## Google Identity Services failure pattern

Symptoms:
- Browser console points at `https://accounts.google.com/gsi/transform`.
- Sign-in popup/iframe opens but redirect/session handoff to dashboard fails or is blocked.
- Backend auth may be healthy; the failure is often browser policy rather than credential verification.

Checks:
```bash
curl -fsSI https://<domain> | tr -d '\r' | sed -n '/content-security-policy/Ip;/cross-origin-opener-policy/Ip;/cross-origin-resource-policy/Ip'
```

Known-good Express/Helmet adjustments for GIS:
```ts
helmet({
  crossOriginOpenerPolicy: { policy: 'same-origin-allow-popups' },
  crossOriginResourcePolicy: { policy: 'cross-origin' },
  contentSecurityPolicy: {
    directives: {
      frameSrc: ["'self'", 'https://accounts.google.com', 'https://*.google.com'],
      imgSrc: ["'self'", 'data:', 'https:', 'https://lh3.googleusercontent.com', 'https://*.googleusercontent.com', 'https://*.gstatic.com'],
      scriptSrc: ["'self'", 'https://accounts.google.com', 'https://accounts.googleusercontent.com', 'https://*.gstatic.com'],
      connectSrc: ["'self'", 'https://accounts.google.com', 'https://accounts.googleusercontent.com', 'https://www.googleapis.com', 'https://*.googleapis.com', 'https://*.gstatic.com'],
    },
  },
})
```

Why COOP matters: GIS uses popup/iframe flows; Helmet's default `Cross-Origin-Opener-Policy: same-origin` can break the popup communication path. Use `same-origin-allow-popups` for pages that host GIS.

## Supabase env passthrough in Vite + Docker

If the user gives Supabase values, treat anon/publishable keys as public-but-sensitive enough not to echo repeatedly. Store in env and verify masked as `set/missing`.

For Vite frontend builds in Docker, runtime env is not enough. Pass values as Docker build args and expose them as `ENV` before `npm run build`:
```Dockerfile
FROM deps AS builder
ARG VITE_SUPABASE_URL
ARG VITE_SUPABASE_PUBLISHABLE_KEY
ENV VITE_SUPABASE_URL=${VITE_SUPABASE_URL}
ENV VITE_SUPABASE_PUBLISHABLE_KEY=${VITE_SUPABASE_PUBLISHABLE_KEY}
COPY . .
RUN npm run build
```

In `docker-compose.yml`, add both build args and runtime env using simple `${VAR:-}` expansion. Avoid nested Compose defaults like `${A:-${B:-}}`; they are easy to misparse and may fail `docker compose config`.

Verification:
```bash
docker compose config >/tmp/compose.out && echo compose_config=ok
npm run build:server && npm run build:web
bash scripts/deploy.sh
curl -fsS http://127.0.0.1:3000/api/health
curl -fsS https://<domain>/api/health
docker compose exec -T app sh -c 'for k in SUPABASE_URL SUPABASE_PUBLISHABLE_KEY SUPABASE_ANON_KEY; do eval v=\$$k; [ -n "$v" ] && echo "$k=set" || echo "$k=missing"; done'
```

## Supabase agent skills install

When the user asks for `skills npx skills add supabase/agent-skills`, execute:
```bash
npx skills add supabase/agent-skills --yes --global
```

Expected installs:
- `supabase`
- `supabase-postgres-best-practices`

Because Hermes skill discovery may be cached in the current session, the installed skills may be available in future sessions even if the current `skills_list` snapshot was already injected.
