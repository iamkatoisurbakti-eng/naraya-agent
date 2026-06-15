# ASPRI Login Panel Auth Gate

Use this when user asks to add a login panel to the static ASPRI mobile app at `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`.

## Implementation pattern

1. Keep it frontend-only unless user explicitly asks for server-backed accounts.
   - Store demo/local profile in `localStorage`, e.g. `aspri_auth_profile_v1`.
   - Store current browser session in `localStorage`, e.g. `aspri_auth_session_v1 = active`.
   - Do not hardcode server credentials or production secrets.

2. Add CSS before the existing modules-disabled/util section:
   - `.login-screen`
   - `.login-hero`
   - `.login-card`
   - `.login-tab`
   - `.login-input`
   - `.login-btn`
   - `.login-status`
   - `.logout-btn`

3. Add a login screen before HOME:
   - `<div id="s-login" class="screen login-screen active">`
   - Include logo `../LOGO APP.png`.
   - Include two modes: `Masuk` and `Daftar`.
   - Inputs: name/phone and 4-8 digit PIN.
   - Submit button text changes by mode.

4. Remove active state from HOME:
   - Replace `<div id="s-home" class="screen active">` with `<div id="s-home" class="screen">`.

5. Add a visible logout control in the HOME header:
   - Use a Tabler logout icon: `<i class="ti ti-logout"></i>`.
   - Call `logoutAspri()`.

6. Add auth helpers in the first inline script near `hist`/`nav`:
   - `getAspriProfile()`
   - `setLoginMode(mode)`
   - `updateAspriUserName(name)`
   - `isAspriLoggedIn()`
   - `showLoginStatus(message, kind)`
   - `submitAspriLogin()`
   - `logoutAspri()`
   - `bootAspriAuth()`

7. Gate navigation:
   - Initialize `hist = ['login']`.
   - In `nav(id)`, if `id !== 'login' && !isAspriLoggedIn()`, show login and stop.
   - In `back()`, if logged out, show login.
   - Call `bootAspriAuth()` after binding login events.

8. Personalize HOME greeting:
   - Change `Halo, <em>Pengguna</em>` to `Halo, <em id="home-user-name">Pengguna</em>`.

## Verification commands

Run from app root:

```bash
python3 - <<'PY'
from pathlib import Path
import re
html = Path('frontend/index.html').read_text()
print('login screen', '<div id="s-login"' in html)
print('home active count', html.count('id="s-home" class="screen active"'))
print('login active count', html.count('id="s-login" class="screen login-screen active"'))
print('logout button', 'logoutAspri()' in html)
js = '\n'.join(re.findall(r'<script>(.*?)</script>', html, flags=re.S))
Path('/tmp/aspri-inline.js').write_text(js)
print('scripts extracted', len(js))
PY
node --check /tmp/aspri-inline.js
systemctl restart aspri-frontend
sleep 1
systemctl is-active aspri-frontend
curl -sS -I http://127.0.0.1:8091/frontend/index.html | head -n 1
```

Use a temp file for HTML content checks; do not combine `curl | python3 - <<'PY'` because the here-doc consumes Python stdin and can make curl report `Failure writing output to destination`:

```bash
tmp=$(mktemp)
curl -sS http://127.0.0.1:8091/frontend/index.html -o "$tmp"
python3 - "$tmp" <<'PY'
from pathlib import Path
import sys
html = Path(sys.argv[1]).read_text()
checks = {
  'login_title': 'Login panel untuk membuka Asisten Pribadi Digital' in html,
  'register_tab': 'login-tab-register' in html,
  'login_storage': 'ASPRI_AUTH_KEY' in html,
  'auth_gate': 'Silakan login dulu untuk membuka modul ASPRI' in html,
  'logout': 'logoutAspri()' in html,
  'home_user': 'home-user-name' in html,
  'login_active': 'id="s-login" class="screen login-screen active"' in html,
  'home_not_active': 'id="s-home" class="screen active"' not in html,
}
for k, v in checks.items():
    print(k, 'PASS' if v else 'FAIL')
PY
rm -f "$tmp"
curl -sS http://127.0.0.1:8090/ | head -c 300
printf '\n'
systemctl status aspri-frontend --no-pager | sed -n '1,8p'
```

## Google-only variant

If the user asks for login to only use Google, do not keep the local PIN/register flow. Use `references/aspri-google-only-login.md` instead of this local profile pattern: remove `login-name`, `login-pin`, local `Daftar`, and generate `user_id` from the Google Identity Services payload (`sub`).

## Pitfalls

- This is not real multi-device authentication. It is a local browser lock/profile gate. Say that plainly if relevant.
- Do not place login screen after HOME and leave HOME active; the app will still open directly to Beranda.
- Keep `login` out of `ENABLED_MODULES` unless intentionally making it navigable as a module; `show('login')` works without it.
- If Chromium/browser automation fails with ProcessSingleton/socket directory errors, treat it as environment-blocked after source, HTTP, and JS syntax checks pass.
