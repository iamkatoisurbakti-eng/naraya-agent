# ASPRI UI Cleanup + Systemd Backend Pitfalls

Use for small ASPRI app UI cleanup requests such as hiding/removing sections, labels, buttons, stat counters, or module copy in `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`.

## UI cleanup workflow
1. Locate exact text/IDs with a script rather than guessing:
   - search for the visible text, element id, and related JS constants.
   - Example: `Kirim Pesan Test`, `wa-send`, `wa-to`, `wa-message`.
2. Remove only the requested UI block when possible.
   - For WhatsApp test-message removal, delete the workflow-card containing `Kirim Pesan Test`, `wa-to`, `wa-message`, and `wa-send`.
   - Leaving the JS constants/listeners is acceptable if they null-check (`if (waSendBtn) ...`), but verify syntax and live HTML.
3. For ASPRI BISNIS copy/form cleanup, remove or replace only the business-facing copy requested:
   - `Debat · Backtest · Validasi 24 Jam Nonstop`
   - `Debat multi-agent, backtest, validasi & scoring 24 jam nonstop`
   - `Debat & Backtest Bisnis`
   - `Analisis Strategi Bisnis` when the user asks to remove it.
   - If the user lists the entire strategy form (`Judul Strategi / Perubahan`, `Market`, `Isi Konteks Bisnis`, `Perubahan yang ingin diuji`, `Analisis Bisnis`, `Siap menjalankan evaluasi bisnis.`), delete the whole business `workflow-card` containing `business-title`, `business-market`, `business-content`, `business-change`, `business-run`, `business-status`, and `business-result`. Leave the read-only analysis card and history unless explicitly asked.
4. Home screen small cleanup:
   - If asked to remove stat counters like `5 Modul Aktif`, `0 Jasa Tersedia`, or `AI Powered`, delete the whole Home `.stats-row` block, not just the numbers.
   - If asked to remove `Cari fitur`, delete the whole Home `.search-wrap` block containing `Cari fitur atau layanan...` and optionally remove unused `.search-wrap`/`.search-box` CSS after confirming no remaining HTML usage.
   - Keep similarly named content outside Home only if it is unrelated; if the visible phrase persists live and the user asked generally (e.g. `Jasa Tersedia`), inspect and remove the remaining visible label too.
5. Branding cleanup: if the user says remove `X NUSANTARA`, replace visible `ASPRI X NUSANTARA` with `ASPRI` in `frontend/index.html` and `ASPRI X NUSANTARA Admin` with `ASPRI Admin` in `admin/index.html`; verify `X NUSANTARA` count is 0 in source and live HTML.
6. Button/icon polish: audit for actionable buttons/divs with no `<i>` or `<img>` (e.g. `.promo-cta`, `.kc-action`, `.popular-*`, `.news-btn`, dynamic POS/venue buttons). Add Tabler icons inline, using semantically matched icons (`ti-message-chatbot`, `ti-player-play`, `ti-check`, `ti-external-link`, `ti-copy`, `ti-trash`, `ti-credit-card`). Also update JS branches that rewrite button text (use `innerHTML`, not `textContent`) so icons persist after state changes. For broad visual cleanup, add a class-level CSS polish block: make buttons inline-flex with consistent `gap`, force icon backgrounds transparent, and set logo/image icon containers (`.brand-logo`, `.login-logo`, `.asset-icon`, `.mod-logo`, `.product-thumb`) to transparent backgrounds with `object-fit: contain` so no white/dark boxes appear behind PNG icons.
7. User-ID visibility cleanup: if the user asks to hide USER-ID/user_id from the dashboard, remove visible `USER-ID`, `home-user-id`, `login-user-id`, and help/status text mentioning user_id, but keep Google-derived `profile.user_id`, `generateGoogleUserId()`, `getCurrentAspriUserId()`, and backend payload `user_id: getCurrentAspriUserId()` intact. See `references/aspri-user-id-hidden-backend-only.md`.
8. Verify with both source and live HTML counts: target text should be `0`, and icon audits should show no obvious actionable button without an icon.
8. Restart frontend so changes appear immediately.
6. Verify with both source and live HTML counts: target text should be `0`, and icon audits should show no obvious actionable button without an icon.
7. Restart frontend so changes appear immediately.

## Verification commands
```bash
cd /root/nusantara-agent/aspri-nusantara-app
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile, os
html=Path('frontend/index.html').read_text()
for term in ['Kirim Pesan Test','Analisis Strategi Bisnis','X NUSANTARA','Judul Strategi / Perubahan','Analisis Bisnis']:
    print(term, html.count(term))
# quick actionable-button icon audit
sus=[]
for m in re.finditer(r'<(?:button|a|div)\b([^>]*)>(.*?)</(?:button|a|div)>', html, re.S):
    attrs, inner = m.group(1), m.group(2)
    if any(k in attrs for k in ['gen-btn','create-btn','analyze-btn','ab ','ic-btn','promo-cta','kc-action','news-btn','popular-complete-btn','popular-tutor-btn','pos-paid-btn','learn-done-btn','pos-remove-btn','pos-pay-link-btn']) or m.group(0).startswith('<button'):
        text=re.sub('<[^>]+>',' ',inner); text=' '.join(text.split())
        if text and '<i ' not in inner and '<img ' not in inner and '${' not in text:
            sus.append((html[:m.start()].count('\n')+1, text[:80]))
print('actionable_buttons_without_icons', sus)
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
curl -fsS http://127.0.0.1:8091/frontend/index.html -o /tmp/aspri-index.html
python3 - <<'PY'
from pathlib import Path
html=Path('/tmp/aspri-index.html').read_text()
print('live bytes', len(html))
PY
curl -fsS http://127.0.0.1:8090/
systemctl is-active aspri-backend aspri-frontend
```

## Backend systemd/import pitfall
ASPRI backend may fail after restart if systemd service drifts to:

```ini
WorkingDirectory=/root/nusantara-agent/aspri-nusantara-app/backend
ExecStart=/root/nusantara-agent/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8090
```

because imports like `from backend.datarakyat ...` or `from backend.aspri_chat_agent ...` cannot resolve `backend` from inside the backend directory. Preferred service shape:

```ini
[Service]
Type=simple
WorkingDirectory=/root/nusantara-agent/aspri-nusantara-app
Environment=PYTHONUNBUFFERED=1
EnvironmentFile=-/root/nusantara-agent/.env
ExecStart=/root/nusantara-agent/.venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8090
Restart=always
RestartSec=3
```

If `main.py` contains `from __future__ import annotations`, keep it as the first executable statement. Do not prepend `sys.path` lines above it; that causes `SyntaxError: from __future__ imports must occur at the beginning of the file`.

After changing service files:

```bash
systemctl daemon-reload
systemctl restart aspri-backend
curl -fsS http://127.0.0.1:8090/
```
