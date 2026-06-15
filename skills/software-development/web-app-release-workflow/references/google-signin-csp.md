# Google Sign-In + CSP notes

Session findings:
- Google login was failing because the page CSP blocked Google Identity Services.
- The UI fix that held up best was `google.accounts.id.renderButton(...)` instead of a custom button that only called `prompt()`.
- E2E tests need to stub the same GIS method the UI uses.

Practical details:
- Allow Google GIS script/iframe origins in CSP.
- Keep both env vars aligned for the app:
  - `GOOGLE_CLIENT_ID`
  - `VITE_GOOGLE_CLIENT_ID`
- If production login fails after code changes, check browser console for CSP, GIS, and OAuth origin mismatch errors first.

Test stub pattern:
- Mock `renderButton(container)` to create a test button and invoke the credential callback.
- This keeps the test aligned with the real GIS flow instead of the old custom button path.
