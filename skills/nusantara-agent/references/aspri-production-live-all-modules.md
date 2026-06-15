# ASPRI production live all modules

Use when the user asks to make ASPRI production/live and ensure every module can be used in `/root/nusantara-agent/aspri-nusantara-app`.

## Scope
- Frontend source: `frontend/index.html`.
- Backend feature registry: `shared/features.json`.
- Admin source: `admin/index.html`.
- Services: `aspri-frontend`, `aspri-backend`.

## Steps
1. Audit frontend screens and module gate:
   - Extract `id="s-*" class="screen"` values.
   - Extract `var ENABLED_MODULES = [...]`.
   - Every screen except `login` must be present in `ENABLED_MODULES`.
2. Add production home cards for all user-facing modules:
   - chat, belajar, whatsapp, bisnis, keuangan, produk, jasa, content, bantu, video, berita, datarakyat, emas, design, hobby, ide-bisnis, lacak, modul, pos, sehat.
   - Each card must call `nav('<module>')` and have an icon/logo plus short description.
   - Update visible count to `20 aktif` when these 20 modules are present.
3. Backend registry:
   - Update `shared/features.json` with the same 20 feature keys so `/features` and `/workflow/run` whitelist production modules.
   - Restart backend after changing this file because `FEATURES` is loaded at import time.
4. Admin UI:
   - Add all module options to the admin `#feature` select.
5. Fix module-specific live controls:
   - Ensure `video-generate` has a click listener for `runWorkflow`.
   - Ensure `workflow-feature` change triggers `syncWorkflowTemplates`.
   - If ASPRI EMAS has UI buttons but no JS, wire `emas-search` / `emas-today` to `/workflow/run` with feature `emas` and render the result in `emas-result`.
   - Be careful when inserting JS strings: use escaped `\n` in regex/string literals, not raw newlines, then verify with `node --check`.
6. Verify source:
```bash
cd /root/nusantara-agent/aspri-nusantara-app
python3 - <<'PY'
from pathlib import Path
import re, json, subprocess, tempfile, os
html=Path('frontend/index.html').read_text()
screens=re.findall(r'id="s-([^"]+)" class="screen', html)
mods=re.findall(r"'([^']+)'", re.search(r'var ENABLED_MODULES = \[([^\]]+)\]', html).group(1))
print('not_enabled', sorted(set(s for s in screens if s!='login')-set(mods)))
print('features_count', len(json.loads(Path('shared/features.json').read_text())['features']))
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
```
7. Restart and production smoke:
```bash
systemctl restart aspri-frontend aspri-backend
for i in $(seq 1 20); do curl -fsS http://127.0.0.1:8090/ && break || sleep 1; done
curl -fsS http://127.0.0.1:8090/features
curl -fsS http://127.0.0.1:8091/frontend/index.html -o /tmp/aspri-index.html
curl -fsS https://aspri.nusantara-ai.online/frontend/index.html -o /tmp/aspri-domain-index.html
curl -fsS https://aspri.nusantara-ai.online/features
```
8. API smoke endpoints to cover live modules:
   - `/learning/materials`, `/business/evaluations`, `/keuangan/evaluations`, `/modul/evaluations`, `/design/evaluations`, `/pos/invoices`, `/hobby/arenafinder/venues`, `/lacak/trackings`, `/datarakyat/catalog`, `/news/providers`, `/workflow/templates?feature=video`, `/workflow/templates?feature=emas`.
   - POST `/workflow/run` for at least `video` and `emas` because those controls depend on the shared workflow runner.

## Pitfalls
- The backend may take a few seconds to bind port 8090 after restart; retry health checks instead of declaring failure immediately.
- Browser automation can fail on this host because of Chrome profile/socket singleton errors. If HTTP/live source checks pass, report browser as environment-blocked, not app-failed.
- Do not expose secrets in UI or final response.
