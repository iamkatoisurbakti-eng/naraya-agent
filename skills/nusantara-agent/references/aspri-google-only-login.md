# ASPRI Google-only Login Pattern

Use when the user asks for ASPRI login to work only with Google, or to remove local name/PIN registration from `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`.

## Scope

This pattern is frontend-only Google Identity Services for the static ASPRI app unless the user explicitly asks for server-backed OAuth/session validation.

## Implementation steps

1. Add Google Identity Services in `<head>`:

```html
<meta name="google-signin-client_id" content="">
<script src="https://accounts.google.com/gsi/client" async defer></script>
```

Keep the Client ID slot empty if the real OAuth client ID is unavailable; do not invent or hardcode secrets. Tell the user to fill `content="<Google OAuth Web Client ID>"` or expose `window.ASPRI_GOOGLE_CLIENT_ID`.

If the user provides a downloaded Google OAuth JSON such as `client_secret_...apps.googleusercontent.com.json`, parse it locally and use only `web.client_id` in the frontend meta tag. Never paste, echo, or embed `web.client_secret` in HTML, logs, or the final response. Confirm the JSON `web.javascript_origins` contains the production ASPRI origin (currently `https://aspri.nusantara-ai.online`) and mention if Google Console must be updated.

2. Replace the local login/register/PIN card:
- Remove `login-name`, `login-pin`, `login-tab-register`, `PIN Akses`, and local `Daftar` UI.
- Add `#google-signin-button` for GIS renderButton.
- Add a fallback button that only reports missing Client ID; it must not create a fake login.

3. Auth helpers:
- Decode GIS credential JWT payload client-side for local profile display.
- Generate stable user_id from Google subject: `aspri-google-<payload.sub>`.
- Store profile with `provider: 'google'`, `google_sub`, `email`, `name`, `picture`, `user_id`, `last_login_at` in localStorage.
- `isAspriLoggedIn()` must require `profile.provider === 'google'` and a `user_id`.

4. Keep API payloads user-specific:
- Replace hardcoded `user_id: 'aspri-...-user'` / `aspri-web-user` with `user_id: getCurrentAspriUserId()` across chat, workflow, learning, POS, finance, product-related calls, etc.
- Replace URL query hardcodes like `/learning/materials?user_id=aspri-belajar-user` with `'/learning/materials?user_id=' + encodeURIComponent(getCurrentAspriUserId())` so progress/data stays per Google account.

5. If a Google OAuth JSON is stored in the static app root, harden `serve_frontend.py` so static HTTP cannot serve secrets:
- deny names starting with `client_secret`
- deny `*_secret.json`
- deny `google_token.json`
- deny dotfiles if possible
Then verify the secret URL returns 404/403 locally and on the public domain.

6. Navigation gate:
- Keep `s-login` active before HOME.
- Keep HOME not active in source.
- `nav(id)` redirects to login when `!isAspriLoggedIn()`.

## Verification commands

```bash
cd /root/nusantara-agent/aspri-nusantara-app
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile, os
html=Path('frontend/index.html').read_text()
checks={
 'google_script':'accounts.google.com/gsi/client' in html,
 'google_meta':'google-signin-client_id' in html,
 'google_client_id_not_empty': bool(re.search(r'<meta name="google-signin-client_id" content="[^"]+\.apps\.googleusercontent\.com">', html)),
 'no_secret_in_frontend':'client_secret' not in html and 'GOCSPX' not in html,
 'google_button':'google-signin-button' in html,
 'pin_removed':'login-pin' not in html and 'PIN Akses' not in html,
 'register_removed':'login-tab-register' not in html and '>Daftar<' not in html,
 'google_user_id':'generateGoogleUserId' in html and "provider: 'google'" in html,
 'api_user_id':'user_id: getCurrentAspriUserId()' in html,
 'no_learning_user_hardcode':'aspri-belajar-user' not in html,
 'login_active':'id="s-login" class="screen login-screen active"' in html,
 'home_not_active':'id="s-home" class="screen active"' not in html,
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
systemctl is-active aspri-frontend aspri-backend
curl -fsS http://127.0.0.1:8090/ | head -c 200
# If an OAuth JSON exists in app root, its public URL must not be readable:
curl -sS -o /tmp/aspri-secret-check -w '%{http_code}\n' 'http://127.0.0.1:8091/client_secret_EXAMPLE.apps.googleusercontent.com.json'
curl -fsS https://aspri.nusantara-ai.online/ -o /tmp/aspri-domain-root.html
python3 - <<'PY'
from pathlib import Path
html=Path('/tmp/aspri-domain-root.html').read_text()
print('domain_client_id', 'PASS' if '.apps.googleusercontent.com' in html and 'google-signin-client_id' in html else 'FAIL')
print('domain_no_secret', 'PASS' if 'client_secret' not in html and 'GOCSPX' not in html else 'FAIL')
PY
```

## Pitfalls

- Google button will not work until a real Google OAuth Web Client ID is configured for the served origin. Do not claim end-to-end Google auth is live unless Client ID exists and browser sign-in was tested.
- OAuth JSON files downloaded from Google include `client_secret`; even for Web clients, treat that as sensitive. Extract `client_id` only, and if the JSON remains under the app root, add/verify static-serving denial before reporting success.
- `search_files` may miss strings in large HTML files; for security checks use a direct Python read/count for `client_secret`, `GOCSPX`, old hardcoded user IDs, and the Google Client ID.
- After `systemctl restart`, the backend may need a second before port 8090 accepts connections. If an immediate curl fails but systemd says active, check `systemctl status`, `ss -ltnp`, and retry the health curl.
- A frontend-only decoded GIS credential is suitable for local UI gating, not high-security server auth. For protected backend data, add server-side token verification.
- Do not leave PIN/register fallback active when user says “hanya bisa menggunakan Google”.
- Do not create fake Google login in fallback mode; fallback should report configuration missing.
