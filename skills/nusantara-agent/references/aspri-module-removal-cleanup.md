# ASPRI module removal / cleanup workflow

Use when the user asks to remove or hide specific ASPRI modules from the app.

## Scope
Project root: `/root/nusantara-agent/aspri-nusantara-app`.

Primary files:
- `frontend/index.html` — visible module cards, screens, navigation gate.
- `shared/features.json` — backend `/features` registry and workflow allowlist.
- `admin/index.html` — admin feature dropdown plus any module-specific admin cards/functions that can keep removed labels visible even after the dropdown option is gone.

## Recommended removal levels
1. If the user only says “hapus dari dashboard”, remove the home card and remove the module from `ENABLED_MODULES`.
2. If the user says “hapus ASPRI <module>” without limiting scope, remove/nonactivate it from:
   - `ENABLED_MODULES`.
   - Home module cards.
   - The screen block `<div id="s-<module>" class="screen">...</div>`.
   - `shared/features.json`.
   - Admin `<option value="<module>">...`.
   - Module-specific admin panels/functions that contain removed labels (example: a `Design Evaluation 24h` card can keep `ASPRI DESIGN` visible after removing the `design` option).
   - Any remaining visible `ASPRI <MODULE>` labels in frontend/admin source.
3. Leave backend route implementations in `backend/main.py` unless explicitly asked to delete backend APIs; old data/API endpoints may still be useful and deleting them is riskier.

## Safe screen-block removal technique
Use div-depth parsing rather than brittle regex:
- Find marker: `<div id="s-<module>" class="screen"`.
- Optionally include the preceding `<!-- ========== ... ========== -->` comment if it is near the marker.
- Walk `<div...>` / `</div>` tags from the marker until depth returns to zero.
- Remove that block plus trailing whitespace.

## Home dashboard after removal
- Rebuild the module-card section instead of patching individual cards when removing many modules.
- Update the visible count (for example `11 aktif`) to match remaining user-facing cards.
- Keep `home` in `ENABLED_MODULES` but do not count it as a dashboard module card.

## Verification
Run from the app root:

```bash
python3 - <<'PY'
from pathlib import Path
import re, json, subprocess, tempfile, os
removed=['sehat','modul','pos','video','content','bantu','berita','datarakyat','hobby']
labels=['ASPRI SEHAT','ASPRI MODUL','ASPRI POS','ASPRI VIDEO','ASPRI CONTENT','ASPRI BANTU','ASPRI BERITA','ASPRI DATARAKYAT','ASPRI HOBBY']
html=Path('frontend/index.html').read_text()
admin=Path('admin/index.html').read_text()
features=json.loads(Path('shared/features.json').read_text())['features']
enabled=re.search(r'var ENABLED_MODULES = \[[^\]]+\]', html).group(0)
print('screens_removed', all(f'id="s-{x}"' not in html for x in removed))
print('enabled_removed', all(f"'{x}'" not in enabled for x in removed))
print('features_removed', all(x not in features for x in removed))
print('admin_options_removed', all(f'value="{x}"' not in admin for x in removed))
print('visible_labels_removed_frontend', all(x not in html for x in labels))
print('visible_labels_removed_admin', all(x not in admin for x in labels))
for file in ['frontend/index.html','admin/index.html']:
    scripts=re.findall(r'<script>(.*?)</script>', Path(file).read_text(), flags=re.S)
    fd,path=tempfile.mkstemp(suffix='.js'); os.write(fd, ('\n;\n'.join(scripts)).encode()); os.close(fd)
    try:
        r=subprocess.run(['node','--check',path], text=True, capture_output=True, timeout=30)
        print(file, 'node_check_exit', r.returncode, (r.stdout+r.stderr).strip())
    finally:
        os.remove(path)
PY
/root/nusantara-agent/.venv/bin/python -m py_compile backend/main.py serve_frontend.py
systemctl restart aspri-frontend aspri-backend
for i in $(seq 1 20); do curl -fsS http://127.0.0.1:8090/ && break || sleep 1; done
curl -fsS http://127.0.0.1:8090/features
curl -fsS http://127.0.0.1:8091/frontend/index.html -o /tmp/aspri-index.html
curl -fsS https://aspri.nusantara-ai.online/frontend/index.html -o /tmp/aspri-domain-index.html
curl -fsS https://aspri.nusantara-ai.online/features
```

## Pitfalls
- `grep`/search tools may miss strings in very large HTML files; a Python `Path.read_text().count(...)` audit is more reliable.
- Removing screen HTML can leave JS constants/functions for removed modules. That is acceptable if they null-check DOM elements and `node --check` passes.
- If JS remains that still emits visible removed labels inside strings, replace those labels too, even if the screen is removed, because the user may expect the label count to be zero.
- Admin pages can contain module-specific evaluation panels and JS functions outside the feature dropdown. After removing a module, search the full `admin/index.html` for both `ASPRI <MODULE>` and lowercase keys; remove or neutralize those admin-only panels/functions if they keep the module visible.
- Public Caddy routing may not expose `/admin/index.html` even when the local admin file exists; verify local admin cleanup via `http://127.0.0.1:8091/admin/index.html` and treat a domain 404 as routing state unless the task is specifically to expose admin.
- Backend takes a few seconds to bind after restart; retry health checks before declaring failure.
