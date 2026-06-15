# ASPRI module UI + WhatsApp Web.js notes

Use for ASPRI app work in `/root/nusantara-agent/aspri-nusantara-app` when adding/removing modules or making ASPRI BELAJAR/WHATSAPP live.

## Current deployment shape
- Frontend is served by `aspri-frontend.service` on port `8091` via `serve_frontend.py`.
- Backend FastAPI is `aspri-backend.service` on port `8090`.
- WhatsApp Web.js service is `aspri-whatsapp.service` on loopback port `8092`.
- Restart after UI/backend changes so the user sees changes immediately:
  - `sudo systemctl restart aspri-backend.service aspri-frontend.service`
  - include `aspri-whatsapp.service` when changing `whatsapp-web-service.js` or `package.json`.

## ASPRI module UI pattern
1. Module cards live in `frontend/index.html` inside the `#s-home` "Modul ASPRI" grid.
2. Enabled screens must be listed in the JS `ENABLED_MODULES` array; otherwise `nav(id)` redirects to home.
3. Module registry for backend feature validation lives in `shared/features.json`.
4. Static logos are served by the frontend from repo root, so card images use paths such as `../aspri-belajar.png` or `../23939026-fb13-48f4-bf7a-937c40294075.png`.
5. Keep user-requested module count consistent in the home stat and section label.

## ASPRI BELAJAR usable class cards
- User wanted "Kelas Populer di Indonesia" cards to work when pressed, not a separate unwanted "Materi Live Production Belajar" panel.
- Class cards should use direct click handlers like `onclick="openPopularClass('learn-01')"` plus `data-material-id`.
- `openPopularClass` should load materials if needed, then call `showPopularMaterial`.
- `showPopularMaterial` should reveal `#popular-class-detail`, scroll it into view, fill title/meta/body from `/learning/materials`, and expose `Tandai Selesai` + `Tanya AI Tutor`.
- Progress completion uses `/learning/complete` with `user_id: 'aspri-belajar-user'`.
- Do not re-add large "ASPRI BELAJAR Live Production" / "Materi Live Production Belajar" panels unless explicitly requested; the user corrected this.

## WhatsApp Web.js service pattern
- `package.json` dependencies: `whatsapp-web.js`, `qrcode-terminal`, `express`, `cors`.
- `whatsapp-web-service.js` exposes loopback endpoints:
  - `GET /status`
  - `POST /start`
  - `POST /send`
  - `POST /logout`
- It prints the QR via `qrcode-terminal` to `journalctl -u aspri-whatsapp.service -f`.
- FastAPI proxies public app calls through:
  - `GET /aspri-whatsapp/status`
  - `POST /aspri-whatsapp/start`
  - `POST /aspri-whatsapp/send`
  - `POST /aspri-whatsapp/logout`

## Backend AI route pattern
- Import from local agent client:
  - `from agent.nusantara_client import ask_feature, ask_nusantara`
- Routes:
  - `POST /ai/chat` -> `return await ask_nusantara(req.message, req.user_id)`
  - `POST /ai/feature/{feature}` -> `return await ask_feature(feature, req.message, req.user_id)`
- Existing `/chat` and `/feature/{feature}` can share the same client calls.

## Verification checklist
- Syntax checks:
  - extract inline HTML scripts and run `node --check` on each temporary script
  - `python -m py_compile backend/main.py backend/datarakyat.py agent/nusantara_client.py`
  - `node --check whatsapp-web-service.js`
- HTTP checks:
  - `curl -fsS http://127.0.0.1:8090/health`
  - `curl -fsS http://127.0.0.1:8090/features`
  - `curl -fsS http://127.0.0.1:8090/learning/materials?user_id=aspri-belajar-user&limit=100`
  - `curl -fsS http://127.0.0.1:8092/health` for WhatsApp service
- Live HTML checks should confirm the requested labels/logos/onclick handlers exist in `http://127.0.0.1:8091/`.
