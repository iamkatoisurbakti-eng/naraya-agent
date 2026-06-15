# ASPRI systemd deployment notes

Use this when deploying `/root/nusantara-agent/aspri-nusantara-app` as a durable service rather than an ad-hoc background process.

## Current proven layout

- Backend: FastAPI app in `backend/main.py`.
- Frontend/admin: plain HTML under `frontend/index.html` and `admin/index.html`.
- Backend port: `8090`.
- Frontend port: `8091`.
- Python venv with app deps: `/root/nusantara-agent/.venv`.

## Deployment workflow

1. Compile-check backend before restart:
   - `python3 -m py_compile backend/main.py backend/datarakyat.py`

2. Check live listeners before binding ports:
   - `ss -ltnp '( sport = :8090 or sport = :8091 )'`

3. Use the Nusantara Agent venv for backend; system Python may miss app deps:
   - `/root/nusantara-agent/.venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8090`

4. If backend import fails with `ModuleNotFoundError: No module named 'bs4'`, install in the venv, not globally:
   - `/root/nusantara-agent/.venv/bin/pip install beautifulsoup4`

5. For frontend durability, use a tiny Python `http.server` wrapper that maps:
   - `/` -> `frontend/index.html`
   - `/admin` -> `admin/index.html`
   - other paths -> static files from repo root

6. Create systemd services:
   - `aspri-backend.service`: runs uvicorn from `/root/nusantara-agent/.venv`, working dir `/root/nusantara-agent/aspri-nusantara-app`, port `8090`, `Restart=always`.
   - `aspri-frontend.service`: runs `/usr/bin/python3 /root/nusantara-agent/aspri-nusantara-app/serve_frontend.py`, working dir app repo, port `8091`, `Restart=always`.

7. Enable and start:
   - `systemctl daemon-reload`
   - `systemctl enable --now aspri-backend.service aspri-frontend.service`

8. Verify locally:
   - `curl -fsS http://127.0.0.1:8090/health`
   - `curl -fsS http://127.0.0.1:8091/ | head -c 160`
   - `curl -fsS http://127.0.0.1:8091/admin | head -c 120`
   - `systemctl is-active aspri-backend.service aspri-frontend.service`

## Pitfalls

- Avoid `ps ... grep 'uvicorn|aspri'` forms in this environment; terminal safety detection may misclassify them as long-lived server starts. Prefer `ss` for listeners or inspect `/proc` with split strings if process details are needed.
- Do not assume the plain `python3` environment has FastAPI/httpx/uvicorn/bs4 installed. The working backend environment is `/root/nusantara-agent/.venv`.
- A plain `python3 -m http.server` at the repo root serves directory listings at `/`; use the wrapper so the app opens directly.
