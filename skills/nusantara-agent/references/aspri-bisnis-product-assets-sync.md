# ASPRI BISNIS product assets sync

Use when updating `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html` so ASPRI BISNIS can analyze uploaded product photos or products saved in ASPRI PRODUK.

## Pattern
1. ASPRI PRODUK stores catalog data in localStorage key:
   - `aspri_produk_catalog_v1`
   - product shape includes `id`, `name`, `desc`, `price`, `stock`, `image` data URL, `created_at`.
2. ASPRI BISNIS can use a separate localStorage key for selected analysis assets:
   - `aspri_bisnis_assets_v1`
   - asset shape: `id`, `source` (`upload` or `aspri-produk`), `name`, `desc`, `price`, `stock`, `image`, `created_at`.
3. Add UI inside `#s-bisnis`:
   - file input `id="business-photo"` with `accept="image/*"`.
   - preview image `id="business-photo-preview"` using `.product-preview`.
   - select `id="business-product-sync"` populated from `produkItems`.
   - button `id="business-sync-product"` to copy selected ASPRI PRODUK item into business assets.
   - button `id="business-clear-assets"` to clear selected assets.
   - grid `id="business-asset-grid"` to preview selected assets.
   - button `id="business-analyze"` to send an analysis prompt to ASPRI CHAT.
4. Load/render behavior:
   - `loadProdukCatalog()` should call `renderBusinessProductOptions()` after `renderProdukCatalog()` so the sync dropdown stays current.
   - Add `loadBusinessAssets()` during boot after `loadProdukCatalog()`.
   - Cap business assets (e.g. six) to avoid oversized localStorage from many image data URLs.
5. Analysis behavior:
   - Build a concise text prompt from selected assets including name, price, stock, and description.
   - Call `nav('chat')`, then `sendMessageToNusantara(prompt)`.
   - Do not send raw image data URLs to chat/backend unless the backend explicitly supports image payloads.

## Pitfalls
- When inserting JavaScript via Python string replacement, escape newline literals as `\\n` in JS strings. A raw newline inside `'...'` causes `SyntaxError: Invalid or unexpected token` in `node --check`.
- Keep ASPRI PRODUK persistence client-side unless the user explicitly asks for backend/multi-user storage.
- Existing ASPRI app is static HTML + localStorage; avoid adding build steps or framework assumptions.

## Verification
Run from app root:

```bash
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile, os
html=Path('frontend/index.html').read_text()
checks={
 'business_photo_input':'id="business-photo"' in html,
 'business_photo_preview':'id="business-photo-preview"' in html,
 'business_sync_select':'id="business-product-sync"' in html,
 'business_sync_button':'id="business-sync-product"' in html,
 'business_asset_grid':'id="business-asset-grid"' in html,
 'business_analyze':'id="business-analyze"' in html,
 'business_assets_storage':'aspri_bisnis_assets_v1' in html,
 'sync_function':'syncSelectedBusinessProduct' in html,
 'upload_function':'handleBusinessPhotoUpload' in html,
 'produk_storage':'aspri_produk_catalog_v1' in html,
}
for k,v in checks.items(): print(k, 'PASS' if v else 'FAIL')
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
systemctl restart aspri-frontend aspri-backend
curl -fsS http://127.0.0.1:8091/frontend/index.html -o /tmp/aspri-index.html
curl -fsS http://127.0.0.1:8090/
systemctl is-active aspri-frontend aspri-backend
```
