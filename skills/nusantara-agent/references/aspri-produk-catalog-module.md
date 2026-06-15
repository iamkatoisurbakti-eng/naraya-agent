# ASPRI PRODUK catalog module

Use when adding or maintaining the ASPRI PRODUK frontend module in `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`.

## Pattern
1. Verify the logo exists at project root and is served by the frontend service:
   - Asset used in this session: `0a66ec90-f020-4a9c-b6ac-9ea349c12eb4.png`.
   - Reference from `frontend/index.html` as `../0a66ec90-f020-4a9c-b6ac-9ea349c12eb4.png`.
   - Verify via `curl -I http://127.0.0.1:8091/0a66ec90-f020-4a9c-b6ac-9ea349c12eb4.png`.
2. Add a Home module card:
   - Class: `mod mc-produk aspri-produk-card`.
   - `onclick="nav('produk')"`.
   - Short visible copy: `ASPRI PRODUK` and product catalog description.
3. Add a full screen `id="s-produk"` with:
   - Product name: `produk-name`.
   - Product description: `produk-desc`.
   - Product price: `produk-price`.
   - Product image upload: `produk-image` with preview `produk-preview`.
   - Product stock: `produk-stock`.
   - Save/reset buttons: `produk-save`, `produk-reset`.
   - Catalog list: `produk-list`, count `produk-count`.
4. Add `produk` to `ENABLED_MODULES`; otherwise card taps silently return Home.
5. Store the catalog client-side in localStorage with key `aspri_produk_catalog_v1` unless the user explicitly asks for backend persistence.
6. Use existing helpers when possible:
   - `parseAmount()` for price parsing.
   - `formatMoney()` for Rupiah display.
   - `financeToday()` for compact timestamps.
   - `cleanText()` before rendering user-entered fields.
7. Add event listeners after DOM constants:
   - image change -> preview via FileReader data URL.
   - save -> validate name/description/price and persist.
   - reset -> clear form and preview.
8. Keep image data URLs small enough for localStorage; for production multi-user persistence, move uploads to backend storage instead.

## Verification
Run from app root:

```bash
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile, os
html=Path('frontend/index.html').read_text()
for term in ['ASPRI PRODUK','aspri-produk-card','id="s-produk"','produk-name','produk-desc','produk-price','produk-image','produk-stock','aspri_produk_catalog_v1']:
    print(term, html.count(term))
scripts=re.findall(r'<script>(.*?)</script>', html, flags=re.S)
fd,path=tempfile.mkstemp(suffix='.js')
os.write(fd, ('\n;\n'.join(scripts)).encode()); os.close(fd)
try:
    r=subprocess.run(['node','--check',path], text=True, capture_output=True, timeout=30)
    print('node_check_exit', r.returncode)
    print((r.stdout+r.stderr).strip())
finally:
    os.remove(path)
PY
systemctl restart aspri-frontend
curl -fsS -I http://127.0.0.1:8091/0a66ec90-f020-4a9c-b6ac-9ea349c12eb4.png | head -n 1
curl -fsS http://127.0.0.1:8091/frontend/index.html -o /tmp/aspri-index.html
python3 - <<'PY'
from pathlib import Path
html=Path('/tmp/aspri-index.html').read_text()
for term in ['ASPRI PRODUK','aspri-produk-card','id="s-produk"','produk-name','produk-desc','produk-price','produk-image','produk-stock']:
    print('live', term, html.count(term))
PY
systemctl is-active aspri-frontend aspri-backend
```

## Pitfalls
- Do not add a card without adding `produk` to `ENABLED_MODULES`.
- If the user asks for “gambar produk”, include both file input and visible preview.
- Existing app state uses static HTML and localStorage; do not introduce backend persistence unless requested.
