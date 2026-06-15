# Nusantara AI SaaS UX simplification release notes

Use this reference when turning a live UX audit into production changes for the Nusantara AI SaaS app.

## Pattern that worked
- Treat “lakukan semua perubahan sesuai rekomendasi” as an implementation/deploy request, not another report.
- Make public landing simpler first: remove main-platform news/source widgets, reduce video count, collapse CTA clutter, and ensure no `UpgradeUpgrade`-style duplicate labels.
- Make dashboard task-first: default home should answer “Apa yang ingin dibuat?” with direct cards for Chat AI Gratis, Video, Gambar, Chat Live, and Isi Kredit; keep billing/top-up behind the `Isi Kredit` section instead of rendering it on dashboard home.
- Use progressive disclosure in Studio: keep default model behavior (for example Video Studio default `sora-2`) but hide advanced fields behind `Pengaturan lanjut`.
- For free chat, render `Gratis` / `Kirim Gratis` instead of `0 kredit`.

## Verification targets
- Mobile 390x844 and desktop smoke via terminal Playwright using `/snap/bin/chromium --no-sandbox`.
- Check landing/dashboard scroll height, horizontal overflow, console/page errors, duplicate labels, missing news/source text, task-first dashboard copy, billing hidden on home, Video Studio default Sora 2, and advanced controls initially hidden.
- Update e2e/live-test selectors when removing old dashboard text such as `Total Generate Live` or `Top Up Kredit via AutoGoPay` from the default home.
- If Chromium/Playwright flakes with “Target page/context/browser has been closed” after selector resolution, rerun once after confirming source/build are valid; this occurred as an environment/browser flake.

## Cache/proxy pitfall
- SPA index/root must be `Cache-Control: no-cache, no-store, must-revalidate`.
- Hashed Vite assets under `/assets/*` should be `public, max-age=31536000, immutable`.
- If both Express and Caddy set asset cache headers, live output may show duplicate identical cache directives; acceptable but can be cleaned by having only one layer set them.
- Caddyfile is mounted read-only in Docker Compose. After changing `Caddyfile`, `npm run deploy` may leave the existing Caddy container running and still using stale config. Recreate or reload Caddy and then verify public HTTPS headers directly.

## Backup/deploy notes
- This project may not be a git repo; create manual backups outside the project tree before deploying.
- Do not place copied test files inside the project root because Jest may discover stale tests.
- Verify: `npm run typecheck`, relevant tests/builds, `npm run deploy`, `/api/health`, `docker compose ps`, and live HTTPS browser smoke.
