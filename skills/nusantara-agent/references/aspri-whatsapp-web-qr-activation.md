# ASPRI WhatsApp Web QR activation and OOM triage

Use when ASPRI WHATSAPP QR/start button does not work or QR is only visible in service logs.

## Root cause patterns
- Frontend button can exist but endpoint/proxy wiring may be missing or stale.
- `whatsapp-web-service.js` may generate terminal QR only; mobile users need a rendered image in the ASPRI screen.
- Puppeteer/Chrome can fail with `TargetCloseError: Protocol error (Runtime.evaluate): Target closed` when the host is memory pressured or another WhatsApp bridge owns Chrome sessions.
- `aspri-whatsapp.service` may be active but Chrome may be OOM-killed after `/start`.

## Implementation pattern
Project root: `/root/nusantara-agent/aspri-nusantara-app`.

1. Verify service and proxy:
```bash
systemctl is-active aspri-whatsapp aspri-backend aspri-frontend
ss -ltnp | grep -E ':8090|:8091|:8092'
curl -sS http://127.0.0.1:8090/aspri-whatsapp/status
curl -sS http://127.0.0.1:8092/status
```

2. If QR is terminal-only, add `qrcode` npm dependency and expose a data URL:
```bash
npm install qrcode@^1.5.4
```
In `whatsapp-web-service.js`:
- `const QRCode = require('qrcode');`
- Track `latestQrDataUrl`.
- In `c.on('qr', async (qr) => ...)`, set:
  - `latestQr = qr`
  - `latestQrDataUrl = await QRCode.toDataURL(qr, { margin: 1, width: 320, errorCorrectionLevel: 'M' })`
- Include `latest_qr_data_url` in `/status` response.

3. In `frontend/index.html`:
- Add `wa-qr-box` and `wa-qr-img` under status.
- Render `data.latest_qr_data_url` into `<img>`.
- After POST `/aspri-whatsapp/start`, poll `/aspri-whatsapp/status` every 2 seconds until `has_qr` or `ready`.

## OOM / duplicate bridge triage
If start returns but QR never appears or service logs show OOM/TargetCloseError:
```bash
free -h
ps -eo pid,ppid,comm,%mem,%cpu,rss,args --sort=-rss | head -30
pgrep -a -f 'chrome|chromium|puppeteer|whatsapp-web|wa_api|wa_bridge'
journalctl -u aspri-whatsapp -n 120 --no-pager
```
Actions used successfully:
- Stop/disable duplicate older WhatsApp services if not needed for the current ASPRI UI path.
- Kill stale `wa_api`, `wa_bridge`, or orphan Chrome processes after confirming they are not the target `aspri-whatsapp` service.
- Stop high-memory background jobs temporarily (example: `build_rag_incremental.py`) before starting Puppeteer.
- Restart `aspri-whatsapp`, then POST `/aspri-whatsapp/start` again.

## Verification
```bash
node --check whatsapp-web-service.js
# extract frontend scripts and run node --check on each
/root/nusantara-agent/.venv/bin/python -m py_compile backend/main.py serve_frontend.py
systemctl restart aspri-whatsapp aspri-backend aspri-frontend
curl -sS -X POST http://127.0.0.1:8090/aspri-whatsapp/start
# poll until has_qr=true and latest_qr_data_url starts with data:image/png;base64,
curl -fsS https://aspri.nusantara-ai.online/aspri-whatsapp/status
```

Expected:
- `has_qr: true`
- `latest_qr_data_url` truthy
- domain frontend contains `wa-qr-box`, render function, and polling code.

## Pitfalls
- `systemctl is-active aspri-whatsapp` only proves Node is listening, not that Puppeteer successfully initialized.
- Wait a few seconds after backend restart before local curls; port 8090 can be briefly unavailable.
- Browser automation may be blocked by Chrome ProcessSingleton; HTTP/source verification is sufficient if live endpoints pass.
