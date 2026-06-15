# KSR888 Laravel live-triage notes

Use this note when debugging live KSR888 PHP/Laravel behavior that looks like a UI no-op, login issue, or repeated banner/modal artifact.

## Silent deposit / payment submit
- If a deposit button appears to do nothing, check for a custom JS `submit` handler that calls `event.preventDefault()` and expects JSON.
- Prefer a native form submit for the primary flow unless the JSON path is verified end-to-end.
- After changing Blade around a deposit form, clear compiled views and app cache in the runtime container, then restart the web container.
- On QRIS/manual deposit forms, file inputs can silently block submit when marked `required`; confirm the active deposit flow really needs upload.

## Admin login
- KSR888 admin login should accept either username or email from a single generic `login` field.
- Confirm the target user exists in the live DB and is actually admin-gated with `level` in `[1, 2]` before changing auth code.
- If the login form only posts `name`, align the controller and Blade form together; mismatched field names are a common cause of failed admin sign-in.

## Popup/banner cleanup
- In this codebase, popup banner output may be included from more than one main layout (`layouts/main/main.blade.php` and `layouts/main/master.blade.php`).
- To fully remove a popup banner, remove every include site first, then neutralize or delete the popup partial itself, then clear view cache.
- Verify the served HTML after deploy, not just the source tree, because compiled views can preserve old includes until cache is cleared.
