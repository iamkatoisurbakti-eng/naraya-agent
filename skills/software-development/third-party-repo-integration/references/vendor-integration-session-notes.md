# Vendor Integration Session Notes

This session covered two external repos used as feature sources for ASPRI.

## 1) Leuthra/cek-resi
- Clone path: `/root/.hermes/vendor/cek-resi`
- Repo type: small Node/Hono API that exposes `GET /cek-resi/:number`
- Useful pattern: keep a local fallback tracker in the host app and call the vendor API only when available.
- Lesson: external lookup services can be added as optional enrichment, not as a hard dependency.

## 2) haqiachd/ArenaFinder-Mobile
- Clone path: `/root/.hermes/vendor/ArenaFinder-Mobile`
- Repo type: legacy Android app for finding sports venues and community activities.
- Key artifacts inspected:
  - `README.md`
  - `GUIDE.md`
  - `app/build.gradle`
  - `settings.gradle`
- Host-app mapping used:
  - venue discovery -> `/hobby/arenafinder/venues`
  - booking -> `/hobby/arenafinder/book`
  - join activity -> `/hobby/arenafinder/join`
  - UI card in ASPRI HOBBY for search/book/join flows
- Lesson: do not try to transplant a full Android app into a web stack. Extract the user value and rebuild a lightweight adapter inside the host app.

## Integration heuristics
- Always inspect vendor README/GUIDE first; they often reveal the intended usage faster than code spelunking.
- If the repo is a different platform (Android, PHP, Node service, etc.), map its capabilities into the host app rather than copying its runtime architecture.
- Prefer an internal fallback implementation so the host app still works when the vendor dependency is unreachable.
- Add explicit UI affordances for the imported capability only after the backend surface exists.
