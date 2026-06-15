# ASPRI module production workflow notes

Use for `/root/nusantara-agent/aspri-nusantara-app` when adding or making ASPRI app modules usable in production.

## App/runtime layout
- Frontend: `frontend/index.html` served by `serve_frontend.py` on `aspri-frontend.service` port `8091`.
- Backend: `backend/main.py` on `aspri-backend.service` port `8090`.
- WhatsApp Web.js sidecar: `whatsapp-web-service.js` on `aspri-whatsapp.service` port `8092`, proxied via FastAPI `/aspri-whatsapp/*` endpoints.
- Feature registry: `shared/features.json`; `/features` reflects this file.
- Static assets are served from repo root; module cards can reference assets as `../asset.png` from `frontend/index.html`.

## Adding a module card
1. Confirm the logo exists with `file`/`stat`.
2. Add/update the module card in the home `mod-grid` and update the “Modul Aktif” count and `sec-link` count.
3. Add the module id to `ENABLED_MODULES`; otherwise `nav(id)` silently redirects to home.
4. If a dedicated screen is needed, add `<div id="s-<module>" class="screen">...` plus bottom nav entries.
5. Add/update `shared/features.json` so `/features` matches the visible modules.
6. For admin visibility, add the option/template in `admin/index.html` if the module should appear there.

## ASPRI BELAJAR usability pattern
- Kelas Populer cards are usable when each `.kcard` has `data-material-id` matching live backend seed IDs (`learn-01`..`learn-06`).
- Load live material/progress from `/learning/materials?user_id=aspri-belajar-user&limit=100`.
- Mark completion through `/learning/complete` with `{material_id, user_id}`.
- Add a details panel (`popular-class-detail`) and JS helpers: `loadPopularClasses`, `showPopularMaterial`, `completePopularClass`, `askTutorForPopularClass`.
- If the user asks for “materi live production belajar”, put the material creation/evaluation panel inside `s-belajar`, not `s-sehat`: include `learn-title`, `learn-category`, `learn-content`, `learn-evaluate`, `learn-status`, `learn-result`, `learn-level`, `learn-completed`, and `learn-materials`, wired to `/learning/evaluate`, `/learning/materials`, and `/learning/complete`.
- Verify screen placement by checking the phrase/IDs fall between `id="s-belajar"` and `<!-- ========== SEHAT`; older duplicate learning UI in `s-sehat` can make naive text insertion land in the wrong screen.
- Keep the UI label simple; if the user asks to remove “ASPRI BELAJAR Live Production”, remove that visible section/title while preserving functional popular-class/live-material behavior.
- For deterministic `/learning/evaluate` approval in smoke tests, use enough content and include terms that boost the local scorer: `langkah`, `contoh`, `latihan`, `tips`, `cara`, `template`, `praktik`, `implementasi`, `kelas`, `modul`.
## WhatsApp Web.js module pattern
- Add `package.json` dependencies: `whatsapp-web.js`, `qrcode-terminal`, `express`, `cors`.
- Sidecar service should bind to `127.0.0.1:8092`, store LocalAuth data under `data/whatsapp-webjs-auth`, and expose `/health`, `/status`, `/start`, `/send`, `/logout`.
- Print QR to service logs with `qrcode-terminal`; instruct user to run `journalctl -u aspri-whatsapp.service -f` after clicking Start.
- Proxy through FastAPI endpoints `/aspri-whatsapp/status`, `/start`, `/send`, `/logout` so the frontend can call port `8090` only.

## AI backend endpoints
- Import `from agent.nusantara_client import ask_nusantara, ask_feature` in `backend/main.py`.
- Add/keep:
  - `POST /ai/chat` -> `return await ask_nusantara(req.message, req.user_id)`
  - `POST /ai/feature/{feature}` -> `return await ask_feature(feature, req.message, req.user_id)`
- Existing `/chat` and `/feature/{feature}` may also delegate to those helpers; keep feature existence checks for `/feature/{feature}`.

## Verification
- Syntax: `node --check` extracted inline frontend/admin scripts; `python -m py_compile backend/main.py backend/datarakyat.py agent/nusantara_client.py`; `node --check whatsapp-web-service.js` when WhatsApp exists.
- Restart: `systemctl restart aspri-backend.service aspri-frontend.service` and include `aspri-whatsapp.service` when changed.
- Live checks: `/health`, `/features`, module-specific endpoints, frontend HTML contains expected module/detail IDs, and services are `active`.

## Pitfalls
- Search tools may miss strings in large HTML; use a small Python `Path.read_text().find()` when needed.
- Avoid leaving visible labels the user asked to remove, e.g. “ASPRI BELAJAR Live Production”.
- Do not show internal command transcript clutter in final responses unless the user asks; summarize verification results instead.
- When inserting JavaScript via Python strings, escape newline regexes as `/\\n/g`; otherwise `node --check` can fail with “Invalid regular expression: missing /”.
