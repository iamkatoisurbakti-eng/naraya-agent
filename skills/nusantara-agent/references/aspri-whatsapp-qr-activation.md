# ASPRI WhatsApp Web QR activation notes

Use when ASPRI WHATSAPP Start / Generate QR does not respond, QR only appears in service logs, or whatsapp-web.js fails to start.

## Components
- Frontend: `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`
  - Button: `#wa-start`
  - Status/result: `#wa-status`, `#wa-result`
  - Should include QR image container (`#wa-qr-box`, `#wa-qr-img`) and polling after start.
- FastAPI proxy: `/root/nusantara-agent/aspri-nusantara-app/backend/main.py`
  - `/aspri-whatsapp/status`
  - `/aspri-whatsapp/start`
  - `/aspri-whatsapp/logout`
  - Proxies to `ASPRI_WHATSAPP_WEB_URL`, default `http://127.0.0.1:8092`.
- Node service: `/root/nusantara-agent/aspri-nusantara-app/whatsapp-web-service.js`
  - systemd unit: `aspri-whatsapp.service`
  - package dependencies include `whatsapp-web.js`, `qrcode-terminal`, and `qrcode` for browser-displayable data URLs.

## Known-good behavior
- `POST /aspri-whatsapp/start` returns quickly with `started: true`.
- Within a few seconds, `GET /aspri-whatsapp/status` has either `ready: true` or both:
  - `has_qr: true`
  - `latest_qr_data_url: "data:image/png;base64,..."`
- Frontend renders `latest_qr_data_url` as an `<img>` so the user can scan from the mobile UI; raw `latest_qr` can remain in JSON for debugging.

## Implementation pattern
1. In `whatsapp-web-service.js`, require both QR libraries:
   - `const qrcode = require('qrcode-terminal');`
   - `const QRCode = require('qrcode');`
2. Add state field `latestQrDataUrl` and expose it as `latest_qr_data_url` from `state()`.
3. In the `qr` event, generate both terminal QR and data URL:
   - `latestQr = qr`
   - `latestQrDataUrl = await QRCode.toDataURL(qr, { margin: 1, width: 320, errorCorrectionLevel: 'M' })`
   - `qrcode.generate(qr, { small: true })`
4. Clear `latestQrDataUrl` on `ready` and `logout`.
5. In frontend, render QR image when `data.latest_qr_data_url` exists and poll `/aspri-whatsapp/status` every ~2s after Start until QR/ready/error.

## Verification commands
Run from `/root/nusantara-agent/aspri-nusantara-app`:

```bash
node --check whatsapp-web-service.js
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile, os
html=Path('frontend/index.html').read_text()
for needle in ['wa-qr-box','renderWhatsAppState','latest_qr_data_url','pollWhatsAppQr']:
    print(needle, 'PASS' if needle in html else 'FAIL')
scripts=re.findall(r'<script>(.*?)</script>', html, re.S)
for i,s in enumerate(scripts,1):
    fd,path=tempfile.mkstemp(suffix=f'-{i}.js')
    os.write(fd, s.encode()); os.close(fd)
    r=subprocess.run(['node','--check',path], text=True, capture_output=True)
    print('script', i, r.returncode, (r.stdout+r.stderr).strip())
    os.remove(path)
PY
/root/nusantara-agent/.venv/bin/python -m py_compile backend/main.py
systemctl restart aspri-whatsapp aspri-backend aspri-frontend
systemctl is-active aspri-whatsapp aspri-backend aspri-frontend
curl -sS -X POST http://127.0.0.1:8090/aspri-whatsapp/start
for i in $(seq 1 25); do
  curl -sS http://127.0.0.1:8090/aspri-whatsapp/status > /tmp/aspri-wa-status.json
  python3 - <<'PY'
import json, sys
p=json.load(open('/tmp/aspri-wa-status.json'))
print('event', p.get('last_event'), 'has_qr', p.get('has_qr'), 'qr_img', bool(p.get('latest_qr_data_url')), 'ready', p.get('ready'), 'err', str(p.get('last_error',''))[:80])
sys.exit(0 if (p.get('ready') or (p.get('has_qr') and p.get('latest_qr_data_url')) or p.get('last_event') == 'error') else 1)
PY
  [ $? -eq 0 ] && break || sleep 2
done
curl -fsS https://aspri.nusantara-ai.online/aspri-whatsapp/status
```

## OOM / duplicate-service pitfall
- whatsapp-web.js launches Chromium and can be killed by OOM if other WA bridge services or background RAG/sync jobs consume memory.
- Check memory and duplicate Chrome/WA processes before declaring app code broken:

```bash
free -h
ps -eo pid,ppid,comm,%mem,%cpu,rss,args --sort=-rss | head -30
pgrep -a -f 'chrome|chromium|puppeteer|whatsapp-web|wa_api|wa_bridge' || true
systemctl list-units --type=service --all | grep -Ei 'aspri|whatsapp|wa' || true
```

- If duplicate older WA services are running, stop only the conflicting WA services, not the production `aspri-whatsapp` service:

```bash
systemctl stop nusantara-wa-api nusantara-wa-bridge nusantara-wa-followup nusantara-wa-style-learn || true
```

- If an old process survives unit stop, identify the PID and kill that specific process, then retry QR start. Avoid broad `pkill chrome` on a shared host unless you have verified the process belongs to the stale WA bridge.

## Notes
- A first `/aspri-whatsapp/status` right after restart may return connection failed while Node is binding; retry before treating it as failure.
- If the frontend says Start sent but no QR appears, inspect `journalctl -u aspri-whatsapp -n 120 --no-pager` and `/tmp/aspri-wa-status.json` for `last_error`.
