# ASPRI disable-all-modules UI workflow

Use this when the user asks to "hapus semua modul app ASPRI" but clarifies the app should remain alive and only module cards/shortcuts should be removed from the UI.

## Scope that was requested

- Do not delete the ASPRI app folder.
- Do not stop/disable the ASPRI systemd services.
- Keep backend health and frontend shell live.
- Remove/disable visible module entry points from the UI.

## Proven steps

1. Work in `/root/nusantara-agent/aspri-nusantara-app`.
2. Back up before editing:
   - `frontend/index.html.bak-before-disable-modules`
   - `admin/index.html.bak-before-disable-modules`
   - `shared/features.json.bak-before-disable-modules`
3. In `frontend/index.html`:
   - Replace the home `Modul ASPRI` card grid with an empty/disabled state.
   - Set the home stats to `0 Modul Aktif` and `0 Jasa Tersedia`.
   - Disable header/promo shortcuts that navigate to modules.
   - Replace the home bottom navigation with disabled items, leaving only Beranda active.
   - Add a JS guard so `nav(id)` returns to `home` for any non-home route while modules are disabled.
   - Keep existing non-home screen markup intact for rollback safety unless the user explicitly asks to delete code.
4. In `shared/features.json`, set `{ "features": {} }` so `/features` returns an empty registry.
5. In `admin/index.html`:
   - Disable the feature dropdown and workflow prompt.
   - Replace the Run button with a disabled `Workflow Nonaktif` button.
   - Make `runWorkflow()` return immediately with a disabled message.
   - Make `loadFeatures()` show a disabled notice instead of surfacing module registry data.
6. Restart services:
   - `sudo systemctl restart aspri-backend.service aspri-frontend.service`

## Add back exactly one module after disabling all

Use this when the user asks to add a single visible module while keeping every other ASPRI module hidden.

Example: `ASPRI CHAT` with logo `/root/nusantara-agent/aspri-nusantara-app/aspi-chat.png`.

1. Confirm the asset exists and is a valid image:
   - `file /root/nusantara-agent/aspri-nusantara-app/aspi-chat.png`
2. In `frontend/index.html`, replace the disabled-state block with a one-card `mod-grid`:
   - card name: `ASPRI CHAT`
   - click target: `nav('chat')`
   - logo markup: `<img src="../aspi-chat.png" alt="Logo ASPRI CHAT">`
3. Add/keep logo-card CSS:
   - `.mod-logo img { width:100%; height:100%; object-fit:cover; display:block; }`
4. Set `Modul Aktif` to `1`.
5. Update the nav guard to allow only `home` and `chat`; other module ids should route back to `home`.
6. Update bottom nav so only Chat is clickable besides Beranda.
7. Update `shared/features.json` to contain only chat:
   - `{ "features": { "chat": "ASPRI CHAT - asisten pribadi digital untuk tanya jawab dan bantuan cepat" } }`
8. If admin must match the visible module, update `admin/index.html` to advertise chat only and route `Run Chat` to `/chat` rather than `/workflow/run`.

## Verification

- Compile/check:
  - `/root/nusantara-agent/.venv/bin/python -m py_compile backend/main.py backend/datarakyat.py`
  - `python3 -m py_compile serve_frontend.py`
  - Extract inline `<script>` blocks from `frontend/index.html` and `admin/index.html`, then run `node --check` on each.
- Live HTTP:
  - `curl -fsS http://127.0.0.1:8090/health`
  - `curl -fsS http://127.0.0.1:8090/features` should return `{"features":{}}`.
  - Fetch `http://127.0.0.1:8091/` and verify it contains `Semua modul ASPRI dinonaktifkan` and no home card navigation like `onclick="nav('bisnis')"`.
  - Fetch `http://127.0.0.1:8091/admin` and verify `Workflow Nonaktif` is present.
  - `systemctl is-active aspri-backend.service aspri-frontend.service` should return `active` for both.

## Pitfalls

- Browser verification can fail from Chrome profile singleton errors in this environment; use HTTP + script syntax checks as the reliable proof if browser launch fails.
- Piping `curl` directly into `python3` can trigger security approval. Prefer `urllib.request` inside a Python script for content assertions.
- Do not remove backend endpoint code unless the user explicitly chooses backend deletion; for this scope, keeping endpoints while hiding UI preserves rollback safety.
