# Live port and environment triage

Use this when debugging a local/live app and the observed process or import behavior does not match the code you expect.

## What we learned

- A port can be occupied by a different service than the target app.
- `node /usr/local/lib/hermes-agent/scripts/whatsapp-bridge/bridge.js --port 3000 ...` was listening on port 3000 while the ASPRI app itself was served on port 8090.
- `python3` in this environment could not import `backend.main` because system Python lacked `httpx`.

## Quick verification commands

```bash
ss -ltnp | grep ':3000' || true
ps -fp <pid>
curl -sS http://127.0.0.1:3000/
curl -sS http://127.0.0.1:8090/health
python3 - <<'PY'
from backend.main import app
print(app.title, app.version)
PY
```

## Decision rules

- If the port PID/command does not match the app under investigation, do not change code yet.
- If importing the app fails under system Python, treat it as a runtime/dependency issue and re-run using the correct environment or install missing deps first.
- If the service is already running elsewhere, verify the real serving port before concluding the app is down.

## Notes

Keep this file updated with the actual listening process and interpreter quirks seen in the current environment.
