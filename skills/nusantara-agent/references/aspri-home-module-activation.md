# ASPRI home module activation

Use when the user asks to add/activate a module card on the ASPRI mobile-style frontend, especially modules that already have a screen but are hidden from the home module grid.

Repo: `/root/nusantara-agent/aspri-nusantara-app`
Primary file: `frontend/index.html`

## Steps

1. Verify the asset exists at project root, e.g. `aspri-bisnis.png`.
2. Add the module card inside the Beranda `.mod-grid`:
   - Use `onclick="nav('<module-id>')"`.
   - Use `.mod-icon.mod-logo` with `src="../<asset>.png"`.
   - Keep title, short description, and active badge concise.
3. Add the module id to `ENABLED_MODULES`, otherwise `nav()` will silently send the user back home.
4. Update visible active counts (`Modul Aktif` number and `<n> aktif` label) if the home UI exposes a count.
5. If useful, add/update bottom nav to include the activated module.
6. If the module page exists, add a small hero/logo block near the top using the same asset for visual consistency.
7. Verify with:
   - JS extraction + `node --check`.
   - `curl -I http://127.0.0.1:8091/<asset>.png`.
   - live HTML checks for card class, logo path, enabled module id, and count label.
8. Restart `aspri-frontend`; restart backend only if backend source changed.

## Pitfalls

- Adding a card is not enough: the module must also be in `ENABLED_MODULES`.
- Backend restart can expose Python import path issues. If `backend/main.py` imports a sibling module like `from aspri_chat_agent import ...`, systemd/uvicorn package import may fail with `ModuleNotFoundError`; use package-qualified imports such as `from backend.aspri_chat_agent import ...`.
- The static frontend serves project root on port 8091, so assets referenced from `frontend/index.html` usually use `../asset.png` and verify as `/asset.png` over HTTP.
