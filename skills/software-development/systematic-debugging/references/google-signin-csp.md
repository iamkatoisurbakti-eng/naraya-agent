# Google Sign-In CSP deployment pitfall

Session takeaway:
- Symptom: Google Sign-In button rendered but click/login failed in deployed app.
- Root cause: `helmet()` default CSP blocked Google Identity Services script/frame loads.
- Fix: allow `https://accounts.google.com` and `https://accounts.googleusercontent.com` in CSP directives.

Minimal allowlist used:
- `script-src`: `self`, `https://accounts.google.com`, `https://accounts.googleusercontent.com`
- `frame-src`: `self`, `https://accounts.google.com`
- `connect-src`: `self`, `https://accounts.google.com`, `https://www.googleapis.com`
- `img-src`: `self`, `data:`, `https:`, plus any app-specific remote images already used

Verification:
- Check `content-security-policy` response header includes Google domains.
- Run auth API test that asserts the CSP header contains Google hosts.
- Run auth API suite after patching.

Deployment note:
- Frontend and backend must share the same Google client ID via env wiring during build/deploy.
- If the button is visible but auth fails only in prod, inspect CSP before changing login flow.
- Session-specific detail: when using Google Identity Services, prefer `google.accounts.id.renderButton()` over a custom button that only calls `prompt()`. Keep E2E stubs in sync with the rendered GIS button.
- Another environment pitfall from this session: Playwright webServer startup failed until commands used local binaries such as `./node_modules/.bin/cross-env` instead of assuming a global PATH entry.