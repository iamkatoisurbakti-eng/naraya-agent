# ASPRI UI module toggle workflow

Use this when the user asks to remove, disable, or add ASPRI app modules while keeping the app itself live.

Repo and runtime:
- App root: `/root/nusantara-agent/aspri-nusantara-app`
- Frontend: `frontend/index.html`
- Admin: `admin/index.html`
- Feature registry: `shared/features.json`
- Runtime services: `aspri-backend.service` on `:8090`, `aspri-frontend.service` on `:8091`

Disable all module cards while keeping app alive:
1. Keep service and source intact; do not delete the app directory unless explicitly requested.
2. Replace the home `.mod-grid` cards with an empty/disabled state.
3. Set active module stat to `0` and `/features` registry to `{ "features": {} }`.
4. Add/keep a JS navigation guard so non-enabled modules route back to `home`.
5. Disable admin workflow controls or make them visibly nonactive.
6. Restart both systemd services and verify `/health`, `/features`, frontend root, and admin root.

Add back one or more UI modules:
1. Verify the requested logo path exists and is a valid PNG with `file`/`stat`.
2. Add one `.mod` card to the home module grid with `<div class="mod-icon mod-logo"><img src="../<logo>.png" ...></div>`.
3. Update the count in the stats pill and section link (`N aktif`).
4. Add the module id to `ENABLED_MODULES` so `nav('<id>')` is allowed.
5. Enable any bottom-nav item for that module if the user expects direct navigation.
6. Add the module to `shared/features.json` only for visible/active modules.
7. If admin exposes feature selection, update its local `FEATURE_TEMPLATES` and avoid multi-line single-quoted HTML strings; use template literals or `.map(...).join('')`.
8. Restart `aspri-backend.service` and `aspri-frontend.service`.

Verification checklist:
- `node --check` every inline `<script>` extracted from both `frontend/index.html` and `admin/index.html`.
- `/root/nusantara-agent/.venv/bin/python -m py_compile backend/main.py backend/datarakyat.py`
- `python3 -m py_compile serve_frontend.py`
- `curl -fsS http://127.0.0.1:8090/health`
- `curl -fsS http://127.0.0.1:8090/features`
- Fetch `http://127.0.0.1:8091/` and assert the requested module names/logo filenames/counts are present.
- Fetch each logo from `http://127.0.0.1:8091/<logo>.png` and assert PNG magic bytes.

Pitfalls observed:
- Generic `search_files` may miss literal strings in large HTML; use `read_file` around known offsets or Python substring checks.
- Admin inline JS can break if options are inserted as a raw newline inside single quotes. Always run `node --check` on extracted scripts before restart.
- Browser launch may fail from Chrome ProcessSingleton/profile errors; HTTP + source/JS checks are acceptable primary proof for this ASPRI app.
