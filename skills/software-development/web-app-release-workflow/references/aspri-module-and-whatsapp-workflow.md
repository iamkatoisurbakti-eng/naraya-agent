# ASPRI module enablement and WhatsApp Web.js notes

Use this when the user asks to add/enable ASPRI modules after the app was pared down to a small active set.

## Active-module UI pattern

- Source files:
  - UI: `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`
  - Admin: `/root/nusantara-agent/aspri-nusantara-app/admin/index.html`
  - Feature registry: `/root/nusantara-agent/aspri-nusantara-app/shared/features.json`
  - Backend: `/root/nusantara-agent/aspri-nusantara-app/backend/main.py`
- Add the module card in the home `.mod-grid` with `mod-logo` and the supplied PNG path as `../<file>.png`.
- Update the home counter and section link (`Modul Aktif`, `N aktif`).
- Update `ENABLED_MODULES` so `nav('<module>')` is allowed; otherwise clicks bounce back to home.
- If the module needs a live screen, add `<div id="s-<module>" class="screen">...` and bottom nav entries that only point to active modules.
- Update `shared/features.json`; `/feature/{feature}` rejects modules not present in `FEATURES`.
- If the logo should appear in `/assets`, add the filename to `ASSET_FILES` in `backend/main.py`.

## AI backend endpoint pattern

The ASPRI backend can use the local agent client:

```python
from agent.nusantara_client import ask_feature, ask_nusantara

@app.post("/ai/chat")
async def ai_chat(req: ChatRequest):
    return await ask_nusantara(req.message, req.user_id)

@app.post("/ai/feature/{feature}")
async def ai_feature(feature: str, req: ChatRequest):
    return await ask_feature(feature, req.message, req.user_id)
```

For consistency, `/chat` can delegate to `ask_nusantara(req.message, req.user_id)` and `/feature/{feature}` can delegate to `ask_feature(feature, req.message, req.user_id)` after checking `feature in FEATURES`.

## ASPRI WHATSAPP Web.js module pattern

- Install Node dependencies from the app root with a local `package.json`:
  - `whatsapp-web.js`
  - `qrcode-terminal`
  - `express`
  - `cors`
- Keep the WhatsApp service separate from FastAPI:
  - Node service file: `/root/nusantara-agent/aspri-nusantara-app/whatsapp-web-service.js`
  - systemd service: `aspri-whatsapp.service`
  - local bind: `127.0.0.1:8092`
- Use `LocalAuth` with `dataPath: './data/whatsapp-webjs-auth'` so sessions survive restarts.
- Puppeteer on this server needs sandbox-safe args:
  - `--no-sandbox`
  - `--disable-setuid-sandbox`
  - `--disable-dev-shm-usage`
  - `--disable-gpu`
  - `--no-first-run`
  - `--no-zygote`
- Generate terminal QR with:
  - `qrcode.generate(qr, { small: true })`
- Expose local Node endpoints:
  - `GET /health` and `GET /status`
  - `POST /start`
  - `POST /send`
  - `POST /logout`
- Proxy those through FastAPI for the browser UI:
  - `GET /aspri-whatsapp/status`
  - `POST /aspri-whatsapp/start`
  - `POST /aspri-whatsapp/send`
  - `POST /aspri-whatsapp/logout`

## Verification checklist

Run after edits:

```bash
/root/nusantara-agent/.venv/bin/python -m py_compile backend/main.py backend/datarakyat.py
node --check whatsapp-web-service.js
# Extract inline scripts from frontend/admin and run `node --check` on each temp JS file.
sudo systemctl restart aspri-whatsapp.service aspri-backend.service aspri-frontend.service
systemctl is-active aspri-whatsapp.service aspri-backend.service aspri-frontend.service
curl -fsS http://127.0.0.1:8090/health
curl -fsS http://127.0.0.1:8090/features
curl -fsS http://127.0.0.1:8092/health
curl -fsS http://127.0.0.1:8090/aspri-whatsapp/status
```

To scan QR, start from the UI or POST `/aspri-whatsapp/start`, then watch:

```bash
journalctl -u aspri-whatsapp.service -f
```
