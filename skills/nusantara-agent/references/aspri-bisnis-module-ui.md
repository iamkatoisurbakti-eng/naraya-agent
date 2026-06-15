# ASPRI BISNIS module UI workflow

Use this when the user asks to create/activate/clean ASPRI BISNIS in `/root/nusantara-agent/aspri-nusantara-app`.

## Source of truth
- Frontend: `frontend/index.html`
- Logo asset: `/root/nusantara-agent/aspri-nusantara-app/aspri-bisnis.png`
- Existing screen id: `s-bisnis`
- Module gate: `ENABLED_MODULES`

## Activate ASPRI BISNIS on home
1. Add `bisnis` to `ENABLED_MODULES`:
   - `var ENABLED_MODULES = ['home', 'chat', 'belajar', 'whatsapp', 'bisnis'];`
2. Add a home module card:
   - class: `mod mc-bisnis aspri-bisnis-card`
   - click: `onclick="nav('bisnis')"`
   - logo: `<img src="../aspri-bisnis.png" alt="Logo ASPRI BISNIS">`
3. Update visible active module count (e.g. `4` and `4 aktif`) when adding/removing modules.
4. Optional: add/update bottom nav entry to route to `nav('bisnis')`.
5. On the `s-bisnis` screen, add a compact logo hero using `../aspri-bisnis.png` if requested.

## Copy cleanup preference
When the user asks to remove “Debat · Backtest · Validasi 24 Jam Nonstop” from ASPRI BISNIS, clean all related business UI copy, not only the exact title:
- Business page subtitle mentioning `Debat multi-agent, backtest, validasi ... 24 jam nonstop`
- Workflow title `Debat · Backtest · Validasi 24 Jam Nonstop`
- Button `Debat & Backtest Bisnis`
- Initial status `Siap menjalankan evaluasi multi-agent 24 jam nonstop.`
- Home card copy if it says `debat agent`

Safe replacements used at first pass:
- Subtitle: `Analisis strategi, rekomendasi, dan keputusan bisnis UMKM`
- Title: `Analisis Strategi Bisnis`
- Button: `Analisis Bisnis`
- Status: `Siap menjalankan evaluasi bisnis.`
- Card desc: `Analisis bisnis, strategi UMKM, dan rekomendasi keputusan`

If the user later says to remove `Analisis Strategi Bisnis` or pastes the full strategy form text, remove the entire ASPRI BISNIS workflow form block, not just the heading. Delete the `workflow-card` containing:
- `id="business-title"` / `Judul Strategi / Perubahan`
- `id="business-market"` / `Market`
- `id="business-content"` / `Isi Konteks Bisnis`
- `id="business-change"` / `Perubahan yang ingin diuji`
- `id="business-run"` / `Analisis Bisnis`
- `id="business-status"` / `Siap menjalankan evaluasi bisnis.`
- `id="business-result"`
Keep the static ASPRI BISNIS hero, upload/photo area, analysis-card, and `Riwayat Evaluasi Bisnis` unless explicitly asked otherwise. After removal, verify those exact business form labels/ids count 0 in live HTML.

## Backend deploy pitfall
`aspri-backend` has appeared with two different service shapes during ASPRI work:
- Preferred root service: `WorkingDirectory=/root/nusantara-agent/aspri-nusantara-app` and `python -m uvicorn backend.main:app ...`
- Alternate backend-dir service: `WorkingDirectory=/root/nusantara-agent/aspri-nusantara-app/backend` and `uvicorn main:app ...`

Before changing imports or restart behavior, run `systemctl cat aspri-backend` and match the import style to the active service shape.

If the root service is active and backend flaps with:
`ModuleNotFoundError: No module named 'aspri_chat_agent'`
then `backend/main.py` may contain a stale root import. Use:
`from backend.aspri_chat_agent import ask_aspri_chat`
and ensure no duplicate `from aspri_chat_agent import ask_aspri_chat` remains.

If the backend-dir service is active and backend flaps with:
`ModuleNotFoundError: No module named 'backend'`
then either restore the root service shape or make imports work in both modes. A safe fallback pattern for `backend/main.py` is:
```python
try:
    from backend.aspri_chat_agent import ask_aspri_chat
except ModuleNotFoundError:
    from aspri_chat_agent import ask_aspri_chat
```
Never insert `sys.path` lines above `from __future__ import annotations`; future imports must remain the first executable line or Python raises `SyntaxError: from __future__ imports must occur at the beginning of the file`.

## Verification
Run after edits:
```bash
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile, os
p=Path('/root/nusantara-agent/aspri-nusantara-app/frontend/index.html')
html=p.read_text()
scripts=re.findall(r'<script>(.*?)</script>', html, flags=re.S)
fd,path=tempfile.mkstemp(suffix='.js')
os.write(fd, ('\n;\n'.join(scripts)).encode()); os.close(fd)
try:
    r=subprocess.run(['node','--check',path], text=True, capture_output=True, timeout=30)
    print('node_check_exit', r.returncode)
    print((r.stdout+r.stderr).strip())
finally:
    os.remove(path)
print('bisnis_card', 'aspri-bisnis-card' in html)
print('logo', '../aspri-bisnis.png' in html)
print('enabled', "'bisnis'" in html)
print('old_debat_copy_removed', 'Debat · Backtest · Validasi 24 Jam Nonstop' not in html)
for term in ['Analisis Strategi Bisnis', 'Judul Strategi / Perubahan', 'id="business-title"', 'id="business-market"', 'Isi Konteks Bisnis', 'id="business-run"', 'Siap menjalankan evaluasi bisnis.']:
    print(term, html.count(term))
PY
/root/nusantara-agent/.venv/bin/python -m py_compile backend/main.py backend/aspri_chat_agent.py
systemctl restart aspri-frontend aspri-backend
curl -fsS http://127.0.0.1:8090/
curl -fsS http://127.0.0.1:8091/frontend/index.html -o /tmp/aspri-index.html
curl -I http://127.0.0.1:8091/aspri-bisnis.png
systemctl is-active aspri-backend aspri-frontend
```
