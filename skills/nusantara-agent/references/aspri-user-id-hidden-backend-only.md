# ASPRI user_id hidden from dashboard, still sent to backend

Use when the user asks to hide USER-ID/user_id from the ASPRI dashboard or login UI while keeping per-user backend behavior.

## Scope
- Frontend source: `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`.
- Keep Google-derived `profile.user_id`, `getCurrentAspriUserId()`, and API payloads intact.
- Remove only user-facing display of USER-ID/user_id.

## Implementation pattern
1. Remove visible dashboard/login elements:
   - `home-user-id` span/pill from the Home greeting.
   - `login-user-id` status element from the Login card.
   - visible text like `USER-ID: ...` and help copy mentioning `user_id`.
2. Simplify `updateAspriUserName(name, userId)` so it only updates `home-user-name`; it may keep the `userId` parameter unused for compatibility.
3. Change login success status from `Login Google berhasil. USER-ID: ...` to a generic welcome message.
4. Do not remove or rename:
   - `generateGoogleUserId()`
   - `getCurrentAspriUserId()`
   - `profile.user_id`
   - `user_id: getCurrentAspriUserId()` backend payload fields.

## Verification
Run from app root:

```bash
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile, os
html=Path('frontend/index.html').read_text()
checks={
 'no_visible_USER_ID':'USER-ID' not in html,
 'no_home_user_id':'home-user-id' not in html,
 'no_login_user_id':'login-user-id' not in html,
 'backend_user_id_kept':'user_id: getCurrentAspriUserId()' in html,
 'google_user_id_kept':'generateGoogleUserId' in html,
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
```

## Pitfalls
- Do not remove `user_id` from backend requests; the user only wants it hidden in the dashboard.
- Search for both uppercase `USER-ID` and lowercase `user_id`; lowercase occurrences are expected in JS/backend payload logic, but should not appear in user-facing help text.
- Immediately after restarting backend, curl can race startup. If `systemctl is-active` is active but curl fails, wait/retry once and inspect `systemctl status aspri-backend`.
