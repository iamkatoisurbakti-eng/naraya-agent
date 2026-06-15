# ASPRI BISNIS product photo upload + sync from ASPRI PRODUK

Use when the user asks ASPRI BISNIS to analyze uploaded product photos or reuse products from ASPRI PRODUK.

## Source of truth
- App root: `/root/nusantara-agent/aspri-nusantara-app`
- Frontend: `frontend/index.html`
- ASPRI PRODUK catalog localStorage key: `aspri_produk_catalog_v1`
- ASPRI BISNIS selected asset localStorage key: `aspri_bisnis_assets_v1`

## UI pattern
Add to `s-bisnis`:
- File input: `business-photo` with `accept="image/*"`.
- Preview image: `business-photo-preview` using `.product-preview`.
- Product dropdown: `business-product-sync` populated from ASPRI PRODUK localStorage.
- Sync button: `business-sync-product`.
- Clear button: `business-clear-assets`.
- Asset status: `business-asset-status`.
- Asset grid: `business-asset-grid`.
- Analyze button: `business-analyze`.
- Insight container: `business-insights`.

## JS pattern
1. Keep ASPRI PRODUK functions intact (`loadProdukCatalog`, `saveProdukCatalog`, `renderProdukCatalog`).
2. Add state:
   - `const BUSINESS_ASSET_STORAGE_KEY = 'aspri_bisnis_assets_v1';`
   - `let businessAssets = [];`
   - `let businessUploadImageData = '';`
3. After loading product catalog, call `renderBusinessProductOptions()` so the business dropdown reflects saved products.
4. Implement:
   - `loadBusinessAssets()` / `saveBusinessAssets()`
   - `renderBusinessProductOptions()`
   - `renderBusinessAssets()`
   - `addBusinessAsset(asset)` limited to ~6 items
   - `handleBusinessPhotoUpload()` via FileReader data URL
   - `syncSelectedBusinessProduct()` copies selected ASPRI PRODUK item into business assets
   - `clearBusinessAssets()`
   - `analyzeBusinessAssets()` builds a product-lines prompt and sends it to ASPRI CHAT with `sendMessageToNusantara()`.
5. Add event listeners near the existing product listeners.
6. On boot, call both `loadProdukCatalog()` and `loadBusinessAssets()`.

## Verification
```bash
cd /root/nusantara-agent/aspri-nusantara-app
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
 'produk_module_still_present':'id="s-produk"' in html,
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
python3 -m py_compile serve_frontend.py backend/main.py
systemctl restart aspri-frontend aspri-backend
curl -fsS http://127.0.0.1:8091/frontend/index.html -o /tmp/aspri-index.html
curl -fsS http://127.0.0.1:8090/
```

## Pitfalls
- When generating JS strings from Python, ensure newlines inside JS string literals are escaped as `\n`, not literal line breaks; otherwise `node --check` fails with `SyntaxError: Invalid or unexpected token`.
- LocalStorage data URLs are fine for local/static demo state, but large images can hit browser storage limits. For production multi-device sync, move assets to backend storage.
- Do not break ASPRI PRODUK catalog behavior while adding sync.
