# ASPRI WhatsApp Meta Business redirect

Use when the user asks ASPRI WHATSAPP to connect to WhatsApp Business / Meta instead of local whatsapp-web.js QR.

## Goal
Make ASPRI WHATSAPP use Meta WhatsApp Business / Cloud API as the primary connection path.

## Backend pattern
Project root: `/root/nusantara-agent/aspri-nusantara-app`.

Add/read these env-backed values in `backend/main.py` (do not hardcode secrets):
- `WHATSAPP_APP_ID`
- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_ACCESS_TOKEN`
- `WHATSAPP_VERIFY_TOKEN`
- optional `ASPRI_PUBLIC_BASE_URL`, default `https://aspri.nusantara-ai.online`
- optional `WHATSAPP_META_REDIRECT_URI`

Expose public helper endpoints:
- `GET /aspri-whatsapp/meta-config` returns connect URL, webhook URL, verify URL, and boolean config flags only.
- `GET /aspri-whatsapp/meta-connect` returns a 302 redirect to the Meta URL.

Fallback behavior:
- If `WHATSAPP_APP_ID` is present, build Facebook OAuth dialog URL with scopes:
  `whatsapp_business_management, whatsapp_business_messaging, business_management`.
- If `WHATSAPP_APP_ID` is absent, redirect to:
  `https://business.facebook.com/wa/manage/home/`

Webhook URL for Meta:
- `https://aspri.nusantara-ai.online/whatsapp/webhook`

## Frontend pattern
Update the ASPRI WHATSAPP screen:
- Primary button label: `Konek Meta WhatsApp Business`.
- Subtitle/copy should mention `Meta WhatsApp Business · Cloud API · webhook auto-reply`.
- Keep QR/whatsapp-web.js as legacy only, not the primary connection path.

Critical mobile/browser pitfall:
- Do NOT wait for an async `fetch('/aspri-whatsapp/meta-config')` before navigation. Some mobile browsers or in-app browsers suppress/delay redirect after async work, making the button appear broken.
- Put a direct inline click path on the button, e.g. `onclick="redirectWhatsAppMeta(event)"`.
- The click handler should synchronously set `window.location.href` to `/aspri-whatsapp/meta-connect?redirect_uri=...`.
- `Refresh Config` may still call `/aspri-whatsapp/meta-config` for status display.

Known-good frontend helpers:
```js
function whatsappMetaBaseUrl() {
  const host = window.location.hostname || '76.13.197.168';
  if (host === 'aspri.nusantara-ai.online') return window.location.origin;
  return `${window.location.protocol}//${host}:8090`;
}

function whatsappMetaConnectUrl() {
  return whatsappMetaBaseUrl() + '/aspri-whatsapp/meta-connect?redirect_uri=' + encodeURIComponent(window.location.href);
}

function redirectWhatsAppMeta(event) {
  if (event && event.preventDefault) event.preventDefault();
  window.location.href = whatsappMetaConnectUrl();
  return false;
}
```

## Verification
Run from app root:
```bash
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile, os
html=Path('frontend/index.html').read_text(); py=Path('backend/main.py').read_text()
checks={
 'inline_onclick':'onclick="redirectWhatsAppMeta(event)"' in html,
 'direct_func':'function redirectWhatsAppMeta' in html,
 'connect_url_func':'/aspri-whatsapp/meta-connect?redirect_uri=' in html,
 'meta_config_fetch':'/aspri-whatsapp/meta-config' in html,
 'backend_meta_config':'/aspri-whatsapp/meta-config' in py,
 'backend_meta_connect':'/aspri-whatsapp/meta-connect' in py,
}
for k,v in checks.items(): print(k, 'PASS' if v else 'FAIL')
for file in ['frontend/index.html','admin/index.html']:
    scripts=re.findall(r'<script>(.*?)</script>', Path(file).read_text(), flags=re.S)
    fd,path=tempfile.mkstemp(suffix='.js'); os.write(fd, ('\n;\n'.join(scripts)).encode()); os.close(fd)
    try:
        r=subprocess.run(['node','--check',path], text=True, capture_output=True, timeout=30)
        print(file, 'node_check_exit', r.returncode, (r.stdout+r.stderr).strip())
        if r.returncode: raise SystemExit(r.returncode)
    finally: os.remove(path)
if not all(checks.values()): raise SystemExit('checks failed')
PY
/root/nusantara-agent/.venv/bin/python -m py_compile backend/main.py serve_frontend.py
systemctl restart aspri-backend aspri-frontend
curl -sS -o /tmp/domain-redirect.html -w 'domain_get_status=%{http_code} redirect=%{redirect_url}\n' \
  'https://aspri.nusantara-ai.online/aspri-whatsapp/meta-connect?redirect_uri=https%3A%2F%2Faspri.nusantara-ai.online%2Ffrontend%2Findex.html'
```

Expected:
- Domain `meta-connect` returns `302` with redirect URL to Meta/Facebook Business.
- Live HTML contains `onclick="redirectWhatsAppMeta(event)"`.
- UI no longer uses “Start / Generate QR” as the primary action.
