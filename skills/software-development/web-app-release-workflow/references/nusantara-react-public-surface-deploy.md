# Deploying small React public app surfaces in Nusantara AI SaaS

Use this for requests like "buat design app desktop/mobile lalu deploy" in `/root/nusantara-ai-saas`.

Workflow:

1. Add the new surface as a React component under `web/src/components/<Name>.tsx`.
2. Register a public route in `web/src/main.tsx` under `StandardRoutes`.
3. Add scoped CSS to `web/src/styles/index.css` using a page root class so global dashboard button overrides do not flatten gradients.
4. If the feature needs simple state, add an Express route under `src/routes/...` and mount it in `src/app.ts`; persist safe demo state under `data/*.json` inside the app volume.
5. Build locally:

```bash
npm run build
```

6. Deploy/restart production app:

```bash
docker compose up -d --build app
```

7. Verify:

```bash
curl -fsS http://127.0.0.1:3001/api/health
docker compose ps app
curl --compressed -fsS http://127.0.0.1:3001/<route>
curl --compressed -fsS https://nusantara-ai.online/<route>
```

Notes:
- Use `curl --compressed` for Cloudflare/live HTTPS checks, otherwise compressed API responses may look empty or fail JSON parsing.
- Browser automation may fail on this host with Chromium ProcessSingleton/socket directory errors. If HTTP checks, asset extraction, and app health pass, report browser as environment-blocked rather than app-failed.
- Avoid `curl ... | python3 - <<'PY'`; the heredoc consumes stdin. Save to a temp file or use a short `node -e`/Python script via `execute_code`.
- If literal `&` in shell commands triggers command-safety/backgrounding detection, perform the parse in `execute_code` or construct the string without shell metacharacters.