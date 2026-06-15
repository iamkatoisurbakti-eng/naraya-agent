# Live Uvicorn Route Verification Notes

Session takeaway:
- A stale uvicorn process on the target port can keep serving old behavior even after code changes.
- In this session, `/datarakyat/health` returned 404 on one uvicorn instance while the same route existed in `backend.main.app` when imported through the project virtualenv.
- Importing `backend.main` with the system Python failed because `httpx` was missing; use `./.venv/bin/python` for route inspection and app-level checks in this repo.

Verification pattern:
1. Check which PID is listening on the target port.
2. Import `backend.main:app` using the repo virtualenv Python, not the system interpreter.
3. List routes from `app.routes` and confirm the endpoint path exists.
4. Probe the live endpoint over HTTP.
5. If the live endpoint disagrees with `app.routes`, restart the stale server instance and re-test.

Observed endpoints during this session:
- `/datarakyat/health`
- `/datarakyat/catalog`
- `/datarakyat/modules`
- `/datarakyat/check/{module}/{query:path}`
- `/datarakyat/search`
- `/bantu/whatsapp/config`
- `/bantu/whatsapp/connect`
- `/bantu/whatsapp/autoreply`

Useful commands:
- `ss -ltnp '( sport = :8090 )'`
- `./.venv/bin/python - <<'PY' ... from backend.main import app ... PY`
- `curl -sS http://127.0.0.1:8090/datarakyat/health`
