# Deploy and verification notes

Deploy flow that worked in this repo:
- `bash scripts/deploy.sh`
- The script loads `.env.production` first, then `.env` if present.
- It builds the app image with Docker Compose, starts containers, sleeps briefly, and checks `http://127.0.0.1:3000/api/health`.

Environment notes:
- `.env.production` is the key file for production deploys.
- Production Google login needs both `GOOGLE_CLIENT_ID` and `VITE_GOOGLE_CLIENT_ID`.
- `DOMAIN`, `CLIENT_ORIGIN`, and `JWT_SECRET` also matter for a clean run.

Verification used in this session:
- `npm run build:web`
- API tests for auth/CSP
- Playwright e2e for the landing/auth flow
- `docker compose ps`
- `curl -fsS http://127.0.0.1:3000/api/health`

Pitfall found:
- The Playwright web server command failed when `cross-env` was assumed to be global. Using `./node_modules/.bin/cross-env` fixed it.
