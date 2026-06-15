---
name: codebase-onboarding-engineer
description: "Use when onboarding to an unfamiliar codebase, mapping architecture, discovering workflows, and building a safe first-change plan."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [onboarding, codebase, architecture, discovery, first-change, repository]
    related_skills: [senior-developer, architecture-system-design, writing-plans, subagent-driven-development]
---

# Codebase Onboarding Engineer

## Overview

Use this skill when you are entering a new or unfamiliar codebase and need to understand it quickly without making unsafe assumptions.

## When to Use

Use when you need to:

- map the repo structure and major flows
- identify build, test, and run commands
- understand key modules, entry points, and ownership boundaries
- find the safest first change
- create an onboarding summary or implementation plan

## Working Style

1. Find the entry points and top-level structure.
2. Identify the main runtime, build, and test paths.
3. Trace one feature end-to-end.
4. Note conventions, pitfalls, and local dependencies.
5. Propose a small first change with verification.
   - For KSR888 admin/sidebar audits and live GameXaGlobal counts, see `references/ksr888-sidebar-audit-and-counts.md`.
6. For admin/sidebar work, audit routes and the menu together before editing; split branches and dev-only routes often hide missing links.
- For PHP/Blade fixes on the KSR888 containerized host, remember host files may not be live-mounted. Copy the changed file into `nusantara-ai-saas-ksr888-web-1` and restart the container before verifying the result.
- For local asset-driven mobile sections (provider cards, popup banners, promo art), search the repo for the source folder, normalize filenames into `public/assets/...`, then verify the live HTML and direct asset URLs after container copy.
- If a section appears duplicated on mobile, check the top-level layout includes and breakpoint branches first; the same partial may be rendered twice from different shells.
- After a live content fix, validate both mobile and desktop HTML responses, not only the browser preview.
7. After sidebar edits, re-read the full file to catch duplicated blocks, broken `@else` boundaries, or moved items.
8. For live API totals, prefer a deterministic probe that reads config from the runtime/database and counts fields with `jq` instead of inferring from a sample payload.
9. For KSR888/GameXaGlobal catalog work, derive provider summaries from DB rows: group by `provider_type`, and compute provider-to-game totals from `games.game_provider` because `providers` may not carry a reliable `game_count` column.
10. If the host shell lacks `php`, run lint/smoke checks inside the web container with `docker exec <web-container> php -l ...` before shipping UI/controller edits.
11. For KSR888/GameXaGlobal provider-launch debugging, probe the live container with small deterministic scripts, inspect whether failures are `Player not found` versus `Failed to launch game`, and treat persistent `/slots` fallback as an upstream API/player-resolution issue rather than a frontend routing issue; see `references/ksr888-game-launch-fallbacks.md`.
12. When validating a GameXaGlobal launch helper, reflect the controller inside the live container (with `vendor/autoload.php` loaded) and confirm the payload includes `player_id`, `player_name`, `game_uid`, `provider_code`, `game_type`, `lang`, `currency`, and `lobby_url`; normalize provider/type before launch and remember that KSR888 PHP source may need container rebuild/recreate before the runtime reflects host edits.
13. If a launch error still says `Game belum bisa dibuka. Silakan coba lagi.`, check `fiver->opengame()` argument order and test both provider/game permutations before changing the frontend route.
14. When a launch API is picky, preserve compatibility by sending documented fields plus common aliases (for example `game_code`, `game_id`, `game`, `provider`, `type`) so older endpoints can still resolve the request.
15. After any live PHP controller edit, copy the file into the running KSR888 web container and restart before re-verifying the mobile URL.
13. For KSR888 front provider grids and category pages, read from `SgProvider` active rows for `/slots`, `/casino`, `/sports`, etc. `BgxProvider` can render empty on these surfaces even when `providers` has data. Keep the `detail_url` consistent with `/slots/server-b/{provider_code}/{provider_type}` and verify the live HTML after copying PHP edits into the running web container.
14. When mobile slot/provider pages show duplicate providers, normalize and dedupe by display name in both controller and blade, not by provider code alone. Alias rows like `BNG` vs `Booongo` and `PLAYNGO` vs `Play N Go` should collapse to one rendered card; see `references/ksr888-mobile-provider-dedupe-and-image-verification.md`.
15. For mobile provider/game thumbnails, verify that rendered HTML uses provider API/DB image fields (`frontend_provider_image`, `frontend_mobile_image`, `frontend_banner_image`) and that no `ksr888.online/assets/img` fallback survives in live HTML.
16. For mobile payment/deposit forms on layouts with fixed bottom navs, use a sticky mobile CTA plus extra bottom spacing and keep the submit path as a plain form POST; see `references/mobile-form-verification-and-sticky-cta.md`.
17. For KSR888 homepage header requests like LOGIN/DAFTAR at the top, edit `resources/views/layouts/main/master.blade.php` and verify the rendered HTML order with `curl`; see `references/ksr888-homepage-jackpot-banner-order.md`.


## What to Learn First

- Repository layout
- Frameworks and packages used
- Environment and configuration files
- Test commands and CI expectations
- Key services, modules, or pages
- Common patterns and anti-patterns

## Common Pitfalls

- Jumping into code before understanding the boundaries.
- Missing hidden setup files or env requirements.
- Making a large first change instead of a safe small one.
- Ignoring existing conventions.
- Trusting a server restart log without actually re-checking `/health` after the new process is up.
- Checking only one happy-path sample for a scoring workflow; borderline cases are often where threshold logic shows up.

## Verification Checklist

- [ ] Repo entry points are known
- [ ] Build/test/run commands are identified
- [ ] Key flows were traced
- [ ] Local setup requirements are noted
- [ ] A safe first change path is clear
- [ ] Backend compile/runtime smoke tests are planned for the actual app shape
- [ ] Frontend syntax checks are planned when UI logic lives in static HTML/JS
- [ ] Any server restart required by the app is included in verification

## Web App Verification Notes

If the codebase is a web app with a Python backend plus static frontend/admin pages, use the reference checklist in `references/fastapi-static-webapp-verification.md` for the practical end-to-end verification order.

Common local-runtime pitfall: if a global `uvicorn` is missing, use the repo virtualenv launcher (for example `./.venv/bin/uvicorn`) rather than assuming the system binary exists.

For inline HTML/JS pages, validate each `<script>` block separately when possible; extracting blocks to temp files and running `node --check` catches syntax errors that a browser-only smoke test can miss.

For ASPRI/Nusantara feature-family repos, see `references/aspri-feature-family-verification.md` for the feature map, score-threshold rule (`> 80`), and the preferred restart/smoke-test order. See also `references/aspri-design-evaluation.md` for the dedicated 24h design voting/backtesting loop, persistence, and admin-metric checks. See also `references/aspri-hobby-meetup.md` for the sports-meetup feature, hobby templates, and UI/admin coverage. For resumed sessions after a context drop or handoff, see `references/resume-after-compaction.md`.