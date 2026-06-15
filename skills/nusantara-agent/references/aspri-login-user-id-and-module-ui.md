# ASPRI Login user_id + module UI patterns

Use for ASPRI app requests that touch login/register identity, per-user API routing, or adding/removing mobile-style frontend modules in `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`.

## Login/register user_id pattern

Goal: every registered/login user gets a stable local `user_id` and frontend API calls use that user ID instead of hardcoded module IDs.

Implementation pattern:
1. Keep auth local unless user explicitly requests backend auth. Existing app login stores profile in `localStorage`.
2. Add a multi-user store, e.g. `ASPRI_USERS_KEY = 'aspri_auth_users_v1'`, keyed by normalized name/no. HP.
3. Add `generateAspriUserId(name)` using sanitized name + timestamp + random/crypto suffix:
   - format: `aspri-<safe-name>-<timestamp>-<random>`.
4. On register:
   - reject duplicate normalized name/no. HP.
   - create profile `{ user_id, name, pin, created_at, last_login_at }`.
   - persist both current profile (`ASPRI_AUTH_KEY`) and users map (`ASPRI_USERS_KEY`).
5. On login:
   - lookup by normalized name/no. HP in users map.
   - validate PIN.
   - keep existing `user_id`; create one only for legacy profiles without it.
   - update `last_login_at` and current profile.
6. Migrate legacy profile on boot:
   - if old single-profile auth exists and lacks `user_id`, generate one and save it into users map.
7. Add small UI display:
   - Login panel: `#login-user-id`.
   - Home greeting: `#home-user-id` with a small `USER-ID: ...` pill.
8. Replace hardcoded API payloads like `user_id: 'aspri-web-user'`, `aspri-belajar-user`, `aspri-pos-user`, etc. with:
   - `user_id: getCurrentAspriUserId()`.

Verification:
```bash
cd /root/nusantara-agent/aspri-nusantara-app
python3 - <<'PY'
from pathlib import Path
html=Path('frontend/index.html').read_text()
for term in ['generateAspriUserId','ASPRI_USERS_KEY','home-user-id','login-user-id','user_id: getCurrentAspriUserId()','aspri-web-user']:
    print(term, html.count(term))
PY
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile, os
html=Path('frontend/index.html').read_text()
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
```

Expected checks:
- `generateAspriUserId`, `ASPRI_USERS_KEY`, `home-user-id`, `login-user-id`: present.
- `user_id: getCurrentAspriUserId()`: present in all frontend API payloads that include user_id.
- Old static user IDs such as `aspri-web-user`: absent unless deliberately retained for a non-user scoped system task.
- JS syntax passes.

## Adding a new module with local CRUD

Pattern used for ASPRI PRODUK:
1. Verify root asset over filesystem and HTTP:
   - `test -f <asset>.png && file <asset>.png`
   - `curl -I http://127.0.0.1:8091/<asset>.png`
2. Add module card in Home `.mod-grid` with `onclick="nav('<id>')"`, `.mod-icon.mod-logo`, concise title/description, and active badge.
3. Add module CSS `.mc-<id>` and optional detail styles.
4. Add screen `#s-<id>` with header/back row, hero logo block, form, result/list area, and bottom nav.
5. Add `<id>` to `ENABLED_MODULES`; otherwise nav silently returns home.
6. For local CRUD, use a dedicated `localStorage` key and render/list functions. For image upload previews, use FileReader data URLs.
7. Verify source, HTTP live, and JS syntax, then restart frontend.

## Removing a module from UI

Pattern used for removing Dompet:
1. Count exact visible labels and IDs in source first:
   - `Dompet`, `dompet`, `s-dompet`, `mc-dompet`, `ASPRI DOMPET`.
2. Remove all bottom-nav items pointing to `nav('dompet')`, including active variants.
3. Remove the entire screen block from `<!-- ========== DOMPET ... -->` through its closing `</div>` before the next screen comment.
4. Remove module-specific CSS such as `.mc-dompet`, `.dompet-card`, `.tx-list-dompet`, and related helper classes if no longer used.
5. Recount both source and live HTML; target counts should be zero.
6. Run JS syntax check and restart `aspri-frontend`.

Pitfalls:
- Search tools may miss content in large HTML files; fall back to a Python `Path.read_text().count()`/snippet script.
- Partial file reads are enough for inspection, but use targeted patch/regex to avoid overwriting sibling changes.
- If visible count persists live after removing a Home label, inspect other screens for the same phrase and remove only if the user's wording was general.
