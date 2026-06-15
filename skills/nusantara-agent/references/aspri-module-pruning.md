# ASPRI module pruning and registry cleanup

Use when the user asks to remove/hide ASPRI modules from `/root/nusantara-agent/aspri-nusantara-app`.

## Scope
- Frontend: `frontend/index.html`
- Admin: `admin/index.html`
- Backend registry: `shared/features.json`
- Runtime services: `aspri-frontend`, `aspri-backend`

## Current user preference
The user wants a minimal ASPRI dashboard. Do not re-add removed modules unless explicitly requested. As of the pruning session, removed modules include:
- ASPRI SEHAT
- ASPRI MODUL
- ASPRI POS
- ASPRI VIDEO
- ASPRI CONTENT
- ASPRI BANTU
- ASPRI BERITA
- ASPRI DATARAKYAT
- ASPRI HOBBY

Active visible modules should remain:
- ASPRI CHAT
- ASPRI BELAJAR
- ASPRI WHATSAPP
- ASPRI BISNIS
- ASPRI KEUANGAN
- ASPRI PRODUK
- ASPRI JASA
- ASPRI EMAS
- ASPRI DESIGN
- ASPRI IDE BISNIS
- ASPRI LACAK

## Procedure
1. Audit current state before editing:
```bash
cd /root/nusantara-agent/aspri-nusantara-app
python3 - <<'PY'
from pathlib import Path
import re, json
html=Path('frontend/index.html').read_text()
features=json.loads(Path('shared/features.json').read_text())['features']
print(re.search(r'var ENABLED_MODULES = \[[^\]]+\]', html).group(0))
print(sorted(features))
for mod in ['content','video','bantu','berita','datarakyat','hobby','pos','modul','sehat']:
    print(mod, html.count(f'id="s-{mod}"'), html.count(f"nav('{mod}')"), mod in features)
PY
```
2. Remove module cards from the dashboard section in `frontend/index.html` and update the visible count (e.g. `11 aktif`).
3. Remove the module from `ENABLED_MODULES`.
4. Remove the module screen block `<div id="s-<module>" class="screen">...</div>` if the user asked to delete the module, not merely hide it. A safe way is to count nested `<div>` tags from the screen start until depth returns to zero.
5. Remove the feature key from `shared/features.json`; restart backend because `FEATURES` is loaded on import.
6. Remove matching `<option value="<module>">...` from `admin/index.html`.
7. Search for lingering visible labels (e.g. `ASPRI CONTENT`) and remove/rename stale strings even if they are in leftover helper JS. This prevents old module names from appearing in live HTML/source checks.
8. If a blind text replacement damages JavaScript (example seen: replacing `'content'` left `feature:` with no value or `feature === ||`), patch the syntax immediately and run `node --check`.

## Verification
```bash
cd /root/nusantara-agent/aspri-nusantara-app
python3 - <<'PY'
from pathlib import Path
import json, re, subprocess, tempfile, os
removed=['ASPRI SEHAT','ASPRI MODUL','ASPRI POS','ASPRI VIDEO','ASPRI CONTENT','ASPRI BANTU','ASPRI BERITA','ASPRI DATARAKYAT','ASPRI HOBBY']
ids=['sehat','modul','pos','video','content','bantu','berita','datarakyat','hobby']
html=Path('frontend/index.html').read_text(); admin=Path('admin/index.html').read_text(); features=json.loads(Path('shared/features.json').read_text())['features']
print('labels_removed', all(x not in html for x in removed))
print('screens_removed', all(f'id="s-{x}"' not in html for x in ids))
print('features_removed', all(x not in features for x in ids))
print('admin_removed', all(f'value="{x}"' not in admin for x in ids))
for file in ['frontend/index.html','admin/index.html']:
    scripts=re.findall(r'<script>(.*?)</script>', Path(file).read_text(), flags=re.S)
    fd,path=tempfile.mkstemp(suffix='.js'); os.write(fd, ('\n;\n'.join(scripts)).encode()); os.close(fd)
    try:
        r=subprocess.run(['node','--check',path], text=True, capture_output=True, timeout=30)
        print(file, r.returncode, (r.stdout+r.stderr).strip())
    finally:
        os.remove(path)
PY
/root/nusantara-agent/.venv/bin/python -m py_compile backend/main.py serve_frontend.py
systemctl restart aspri-frontend aspri-backend
for i in $(seq 1 20); do curl -fsS http://127.0.0.1:8090/ && break || sleep 1; done
curl -fsS http://127.0.0.1:8091/frontend/index.html -o /tmp/aspri-index.html
curl -fsS https://aspri.nusantara-ai.online/frontend/index.html -o /tmp/aspri-domain-index.html
curl -fsS https://aspri.nusantara-ai.online/features
```

## Pitfalls
- `search_files` may miss strings in large HTML; use Python `Path.read_text().count()` for exact counts.
- Removing a screen is usually safe because most event listeners are null-guarded, but startup functions may still reference null elements; always run `node --check` and live HTTP checks.
- Backend port 8090 may need a few seconds after restart; retry health before declaring failure.
