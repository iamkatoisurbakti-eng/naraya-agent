# ASPRI BISNIS product photo upload + ASPRI PRODUK sync

Use when the user asks ASPRI BISNIS to analyze product photos or reuse products from ASPRI PRODUK in `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`.

## Source of truth
- Frontend only unless user explicitly requests backend persistence.
- ASPRI PRODUK catalog is stored in browser localStorage key: `aspri_produk_catalog_v1`.
- ASPRI BISNIS selected assets can be stored in browser localStorage key: `aspri_bisnis_assets_v1`.
- Existing screen id: `s-bisnis`; existing product screen id: `s-produk`.

## Implementation pattern
1. In the ASPRI BISNIS screen, add a `workflow-card` before the asset grid with:
   - `input#business-photo[type=file][accept=image/*]`
   - `img#business-photo-preview.product-preview`
   - `select#business-product-sync`
   - `button#business-sync-product` labelled `Sync Produk`
   - `button#business-clear-assets`
   - `div#business-asset-status`
2. Replace static fake upload slots with a dynamic grid:
   - `div#business-asset-grid.up-grid`
   - Empty state: one slot saying `Belum ada foto`.
   - Filled state: image thumbnails from uploaded photos or synced ASPRI PRODUK images.
3. Add JS state near product state:
   - `const BUSINESS_ASSET_STORAGE_KEY = 'aspri_bisnis_assets_v1';`
   - `let businessAssets = [];`
   - `let businessUploadImageData = '';`
4. Add DOM constants for `businessPhotoInput`, `businessPhotoPreview`, `businessProductSync`, `businessSyncProductBtn`, `businessClearAssetsBtn`, `businessAssetStatus`, `businessAssetGrid`, `businessAnalyzeBtn`, and `businessInsights`.
5. Make `loadProdukCatalog()` call `renderBusinessProductOptions()` so the ASPRI BISNIS dropdown stays in sync after ASPRI PRODUK changes.
6. Add helpers:
   - `loadBusinessAssets()` / `saveBusinessAssets()` for localStorage.
   - `renderBusinessProductOptions()` builds dropdown options from `produkItems`.
   - `renderBusinessAssets()` renders selected thumbnails.
   - `addBusinessAsset(asset)` caps selected assets to a small number (e.g. 6).
   - `handleBusinessPhotoUpload()` reads image files as data URLs and adds them to business assets.
   - `syncSelectedBusinessProduct()` copies selected product metadata/image from `produkItems`.
   - `clearBusinessAssets()` resets selected business assets and preview.
   - `analyzeBusinessAssets()` builds a prompt from selected assets and sends it to ASPRI CHAT via `sendMessageToNusantara(...)`.
7. Register event listeners near the existing frontend listeners:
   - `businessPhotoInput.change -> handleBusinessPhotoUpload`
   - `businessSyncProductBtn.click -> syncSelectedBusinessProduct`
   - `businessClearAssetsBtn.click -> clearBusinessAssets`
   - `businessAnalyzeBtn.click -> analyzeBusinessAssets`
8. Call `loadBusinessAssets()` after `loadProdukCatalog()` during boot.

## Pitfalls
- Keep this frontend-only unless backend persistence is requested; current app uses static HTML + localStorage for ASPRI PRODUK.
- Do not sync only text metadata; if a product has `image`, copy the data URL so BISNIS can preview it.
- When generating JS with Python string replacement, escape newline literals as `\\n` inside JS strings. Accidentally writing a literal line break inside single quotes causes `node --check` `SyntaxError: Invalid or unexpected token`.
- Do not remove ASPRI PRODUK while adding sync. Verify both `id="s-produk"` and `id="s-bisnis"` remain.

## Verification
Run from app root:

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
    if r.returncode != 0: raise SystemExit(r.returncode)
finally:
    os.remove(path)
if not all(checks.values()): raise SystemExit('HTML checks failed')
PY
python3 -m py_compile serve_frontend.py backend/main.py
systemctl restart aspri-frontend aspri-backend
systemctl is-active aspri-frontend aspri-backend
curl -fsS http://127.0.0.1:8091/frontend/index.html -o /tmp/aspri-index.html
curl -fsS http://127.0.0.1:8090/ | head -c 160
curl -fsS -o /tmp/aspri-domain-index.html -w '%{http_code}\n' https://aspri.nusantara-ai.online/frontend/index.html
```
