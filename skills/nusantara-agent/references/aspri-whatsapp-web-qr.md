# ASPRI WhatsApp Web QR activation

Use when the ASPRI WHATSAPP module's Start / Generate QR button does nothing, QR only appears in journal logs, or `/aspri-whatsapp/start` / `/aspri-whatsapp/status` fails.

Context:
- App root: `/root/nusantara-agent/aspri-nusantara-app`.
- Frontend: `frontend/index.html`, button `#wa-start`, result/status `#wa-status`, `#wa-result`.
- Backend proxy: `backend/main.py` routes `/aspri-whatsapp/status`, `/aspri-whatsapp/start`, `/aspri-whatsapp/send`, `/aspri-whatsapp/logout`.
- Node service: `whatsapp-web-service.js`, systemd `aspri-whatsapp.service`, local port `127.0.0.1:8092`.
- Public domain proxies backend via Caddy: `https://aspri.nusantara-ai.online/aspri-whatsapp/status`.

Known-good pattern:
1. Verify systemd and ports first:
   ```bash
   systemctl is-active aspri-whatsapp aspri-backend aspri-frontend
   ss -ltnp | grep -E ':8090|:8091|:8092'
   curl -sS -i http://127.0.0.1:8090/aspri-whatsapp/status | head -80
   curl -sS -i http://127.0.0.1:8092/status | head -80
   ```
2. Reproduce via backend, not only browser:
   ```bash
   curl -sS -X POST http://127.0.0.1:8090/aspri-whatsapp/start
   sleep 8
   curl -sS http://127.0.0.1:8090/aspri-whatsapp/status
   journalctl -u aspri-whatsapp -n 120 --no-pager
   ```
3. If QR exists in logs but not UI, install/use Node `qrcode` and make `whatsapp-web-service.js` expose `latest_qr_data_url` in `state()`:
   ```js
   const qrcode = require('qrcode-terminal');
   const QRCode = require('qrcode');
   // state includes latest_qr_data_url
   c.on('qr', async (qr) => {
     latestQr = qr;
     latestQrDataUrl = '';
     latestQrAt = new Date().toISOString();
     latestQrDataUrl = await QRCode.toDataURL(qr, { margin: 1, width: 320, errorCorrectionLevel: 'M' });
     qrcode.generate(qr, { small: true });
   });
   ```
4. Frontend should render an image box and poll after Start:
   - Add `#wa-qr-box` with `#wa-qr-img` near `#wa-result`.
   - `renderWhatsAppState(data)` sets `waQrImg.src = data.latest_qr_data_url` and displays the QR box.
   - `startWhatsAppWeb()` POSTs `/aspri-whatsapp/start`, renders returned state, then polls `/aspri-whatsapp/status` every ~2s until `has_qr` or `ready`.
   - Mask `latest_qr_data_url` in JSON text output so the raw data URL does not flood the UI.
5. Validate syntax:
   ```bash
   node --check whatsapp-web-service.js
   python3 - <<'PY'
   from pathlib import Path
   import re, tempfile, subprocess, os
   html=Path('frontend/index.html').read_text()
   for i,s in enumerate(re.findall(r'<script>(.*?)</script>', html, re.S),1):
       fd,path=tempfile.mkstemp(suffix=f'-{i}.js'); os.write(fd,s.encode()); os.close(fd)
       r=subprocess.run(['node','--check',path],text=True,capture_output=True)
       print('script',i,r.returncode,(r.stdout+r.stderr).strip()[:500]); os.remove(path)
       if r.returncode: raise SystemExit(r.returncode)
   PY
   /root/nusantara-agent/.venv/bin/python -m py_compile backend/main.py
   ```
6. Restart and verify live:
   ```bash
   systemctl restart aspri-whatsapp aspri-backend aspri-frontend
   curl -sS -X POST http://127.0.0.1:8090/aspri-whatsapp/start >/tmp/aspri-wa-start.json
   for i in $(seq 1 25); do
     curl -sS http://127.0.0.1:8090/aspri-whatsapp/status >/tmp/aspri-wa-status.json
     python3 - <<'PY' && break || sleep 2
   import json,sys
   p=json.load(open('/tmp/aspri-wa-status.json'))
   print(p.get('last_event'), p.get('has_qr'), bool(p.get('latest_qr_data_url')), p.get('ready'), str(p.get('last_error',''))[:120])
   sys.exit(0 if (p.get('has_qr') and p.get('latest_qr_data_url')) or p.get('ready') or p.get('last_event')=='error' else 1)
   PY
   done
   curl -fsS https://aspri.nusantara-ai.online/aspri-whatsapp/status -o /tmp/aspri-live-wa.json
   python3 - <<'PY'
   import json
   p=json.load(open('/tmp/aspri-live-wa.json'))
   assert p.get('ok') and ((p.get('has_qr') and p.get('latest_qr_data_url')) or p.get('ready'))
   print('domain ok', p.get('last_event'))
   PY
   ```

Pitfalls:
- `TargetCloseError: Protocol error ... Target closed` plus `kernel OOM killer` in `journalctl -u aspri-whatsapp` means Chrome/Puppeteer was killed for memory, not a frontend click bug. Free memory before retrying.
- Check `free -h` and `ps -eo pid,ppid,comm,%mem,%cpu,rss,args --sort=-rss | head -30`. During one fix, duplicate/old WA services (`nusantara-wa-api`, `nusantara-wa-bridge`, `wa_api`, `wa_bridge.js`) and a large `build_rag_incremental.py` process consumed memory and caused QR generation to fail. Stop/kill nonessential duplicate WA/RAG processes only after confirming scope.
- `systemctl restart aspri-whatsapp` may hang if Puppeteer/Chrome does not exit; systemd may SIGKILL after timeout. Re-check active PID and port after restart.
- If the first `/aspri-whatsapp/status` after restart says connection attempts failed, wait a few seconds for Node service port 8092 before declaring failure.
- Browser automation can fail from Chrome ProcessSingleton/profile conflicts; if HTTP/domain checks prove QR data URL is present and HTML contains `#wa-qr-box`, treat browser as environment-blocked.

Report to user:
- State that the button is wired, QR image appears directly in ASPRI WHATSAPP, and services are active.
- Mention hard refresh/cache clear if the phone still shows the old frontend.
