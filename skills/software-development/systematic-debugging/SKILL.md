---
name: systematic-debugging
description: "4-phase root cause debugging: understand bugs before fixing."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
metadata:
  hermes:
    tags: [debugging, troubleshooting, problem-solving, root-cause, investigation]
    related_skills: [test-driven-development, writing-plans, subagent-driven-development]
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

**File-backed secret pitfall:** if a service uses a local-file credential fallback, verify the file exists in the runtime/container too, not just on the host. Add an explicit path override env if the deployment path differs, and make the file-backed source win over a stale env key when that file is the intended source of truth. See `references/file-backed-secrets-in-containers.md`.

**Primary provider pitfall:** if the file-backed credential is meant to be the main provider (not a fallback), remove the alternate provider path from the business flow and update status/health checks so they report the file-backed provider as authoritative. Test both the request path and the UI labels against that single source of truth. See `references/ksr888-php-register-and-branding.md`.

- **Live-page performance pitfall:** if a page loads but feels slow or noisy, inspect render-time Blade/PHP code for synchronous remote balance/provider calls. Prefer local DB/cache reads on initial render and keep provider refreshes on explicit endpoints or scheduled syncs. See `references/ksr888-live-debugging.md`.
- **Imported PHP host triage pitfall:** if the user asks to fix errors/performance on a live PHP host and explicitly says not to change the appearance, keep the patch functional only. Verify the real served entrypoint (`/index.php` vs `/`, `/mobile/`, `/dekstop/`), clear Laravel caches in-container with a PTY when needed, and use HTTP/Jest smoke checks instead of retrying broken Chromium snap launches. For mobile-only Blade branches, banner/slider removal, and compatibility controllers for missing legacy routes, also see `references/ksr888-mobile-home-ui-cleanup.md`.
- **Popup/banner toggle pitfall:** when the task is only to disable or enable a homepage popup, inspect the live DB value from the running container first, then change `genral_settings.statusPopup` (`1` = off, `0` = on) and verify the rendered HTML from inside the container with a browser-like user agent. Do not trust a host shell that lacks PHP, and do not rely on the presence of `welcomeModal` in script text alone; confirm the modal container is absent/present. See `references/ksr888-popup-banner-toggle.md`.
- **Cache-clear pitfall:** some live containers need an interactive TTY for `php artisan` commands. If `docker compose exec -T ... php artisan optimize:clear` throws Symfony `StreamOutput` errors, first try `--no-ansi`; if that still fails, re-run with an actual PTY (`docker compose exec <service> php artisan optimize:clear --no-ansi`, or terminal tool `pty=true`). Do not assume wrapping `script -qec ... /dev/null` through `exec -T` will fix it; in some containers it still lacks a valid stream.

- **External-asset pitfall:** if the HTML looks clean but the browser still fetches dead third-party images, search runtime data files inside the docroot as well as templates. Replace dead image URLs with a local asset or same-origin proxy/cache layer, not just template text, then verify with live HTTP probes. Preserve the existing layout when fixing these.
- **KSR888 live-debugging note:** when a live page has many asset/runtime errors, inspect the served HTML and backend data first. In this codebase the bad URLs often live in DB-backed game rows, and a server-side image proxy with fallback cache can eliminate DNS/403 noise without changing appearance. See `references/ksr888-live-debugging.md`.
- **Game launch pitfall:** for GameXaGlobal launch failures, verify the documented payload fields (`player_id`, `game_uid`, `lobby_url`, `lang`) before trying alternate aliases, and preserve the returned launch URL exactly instead of rewriting the host. When debugging a mobile complaint, verify one concrete active game end-to-end through `/game_process/{game_code}/{game_provider}` first; if the route redirects to the upstream proxy and then to the provider launch URL, the mobile click path is healthy and any remaining failure is upstream account/agent/token state. If the code needs a local lobby/return URL during tests or CLI execution, build it from `FRONTEND_URL` / `APP_URL` / `APP_PUBLIC_URL` with a relative fallback so `url()` is not required. See `references/ksr888-game-launch-troubleshooting.md`.
- **Imported PHP host admin-login pitfall:** if the user asks to fix admin login on a host like KSR888, inspect the dedicated admin surface (`/support`, `/admin`, `/admins`) before touching auth code. Verify whether the login identifier is username-only or accepts email too, check whether admin access is level-gated (`users.level` in `[1, 2]`), and confirm the live DB row for the target account before assuming the handler is broken. For KSR888, the admin form should accept a generic `login` field and controller-side email-or-name resolution. See `references/ksr888-admin-login-email-or-name.md`.
- **KSR888 mobile home cleanup pitfall:** when the user wants to remove a label/section from the mobile home only, inspect `layouts/main/main.blade.php` first to find the home-route includes. In KSR888, `content.gameNew` is the correct target for removing `GAME BARU` while preserving `GAME TERPOPULAR`. See `references/ksr888-mobile-home-ui-cleanup.md`.
- **Silent submit / no-op pitfall:** if a live deposit or payment button appears to do nothing, inspect whether the page relies on a custom JS `submit` handler that calls `preventDefault()` or expects a JSON response. Verify the rendered button is inside the active form, prefer a native form submit for the primary flow, and clear Blade/view caches after the patch. For KSR888 deposit flows, prefer a server-backed post to `create-payment`/`account/deposit` instead of a JS-only QR generation path unless the JSON response path is proven end-to-end. Also check for hidden optional inputs accidentally marked `required` (for example file upload fields in QRIS/manual modals), because they can block submit with no visible error. See `references/ksr888-silent-deposit-submit.md`.
- **Browser auth pitfall:** if OAuth/Google sign-in works locally but fails after deploy, inspect CSP/network restrictions first. Default security headers can block Google GIS script/frame loads even when the UI button renders. Also verify the GIS flow is actually mounted (`initialize()` + `renderButton()`), not just a custom button that calls `prompt()`. See `references/google-signin-csp.md`.
- **Register-flow pitfall:** when a user says "daftar akun error", reproduce the backend first with a direct POST to the real live registration route, then verify auth/session or API token behavior. If a KSR888-style imported PHP/Laravel hybrid is involved, inspect every registration surface (`/register`, `mobile/function/daftar_akun.php`, `dekstop/function/daftar_akun.php`), the live schema, provider sync, and the post-create redirect target; a successful create can still bounce to home if redirect is wrong, and code may reference columns missing from the live DB. For KSR888 GameXaGlobal player creation, local DB sync, lobby redirects, and always-visible game play buttons, see `references/ksr888-registration-game-buttons.md`. Also see `references/auth-register-debugging.md`, `references/ksr888-php-register-and-branding.md`, and `references/ksr888-registration-api-sync.md`.

- **DB-backed branding / cache-bust pitfall:** when a logo or icon doesn't appear changed after deploy, verify the runtime DB value (e.g. `tb_web.logo`, `tb_web.icon_web`), copy the asset into every live docroot/path the app serves from, and bump the filename or query string to defeat browser/CDN cache. Verify by hashing the served file from inside the container, not just the source tree. See `references/ksr888-php-register-and-branding.md`.
- **Front-end duplication pitfall:** when a user reports a UI element appearing twice and cannot send images, ask for the smallest code snippet first (component/HTML, related CSS, console errors), then inspect the live DOM for duplicate nodes before changing code. See `references/frontend-duplication-checklist.md`.
- **KSR888 GAME TERPOPULAR pitfall:** if the home/mobile popular-games strip looks duplicated or inconsistent, verify whether the same Blade include is rendered twice (for example home + layout) and whether the source collection needs deduping by normalized `game_code` before display. For KSR888 specifically, mobile/desktop branches may need separate rendering paths (`@desktop` / `@elsedesktop`) to avoid cross-branch duplication. See `references/ksr888-game-popular-mobile-duplication.md`. For the 10-item slot-only variant, see `references/ksr888-game-terpopular-slot-top10.md`.
- **Imported PHP mobile/desktop duplication pitfall:** if a section appears twice only on one breakpoint, inspect the top-level layout includes before the child partial. A duplicate can come from the same component being included once in the mobile branch and again in the common shell. Verify the rendered HTML for both user agents and remove the extra include rather than tweaking CSS. See `references/ksr888-mobile-provider-duplication-and-live-sync.md`.
- **Live-container sync pitfall:** if PHP/Blade edits are made on the host but the running KSR888 container doesn't change, copy the edited file into `nusantara-ai-saas-ksr888-web-1` and restart that container before verifying. Host edits are not guaranteed to be live-mounted. See `references/ksr888-mobile-provider-duplication-and-live-sync.md`.
- **KSR888 mobile home ordering / provider dedupe:** when a mobile homepage section must move under the jackpot, change the include order in the mobile layout and place the section directly after the jackpot block in `welcome.blade.php`; don't rely on CSS. For provider strips, dedupe by normalized `provider_code`, require a real image, and bump any cached home catalog key after changing selection logic. See `references/ksr888-mobile-home-ordering-provider-dedupe.md`.
- **KSR888 mobile home ordering pitfall:** when moving `content.home_banner_slider` on mobile, remove it from `resources/views/layouts/main/main.blade.php` and reinsert it in `resources/views/welcome.blade.php` immediately after the progressive jackpot block. This keeps the mobile banner slider below the jackpot without disturbing provider/game sections. Verify with a mobile UA curl and check the rendered order (`jackpot` → `homeBannerCarousel` → `gx-banner-ticker` if present). See `references/ksr888-mobile-home-ui-cleanup.md`.

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-development` skill

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## Hermes Agent Integration

### Investigation Tools

Use these Hermes tools during Phase 1:

- See `references/file-backed-secrets-in-containers.md` for the container/file-credential precedence checklist.
- See `references/auth-register-debugging.md` for the register-flow backend-first verification pattern.
- See `references/register-redirect-flow.md` for duplicated mobile/desktop registration handlers and success-redirect checks.
- See `references/imported-php-host-live-triage.md` for the appearance-preserving live PHP host checklist and PTY cache-clear recipe.
- See `references/ksr888-popup-banner-toggle.md` for the live DB toggle and HTML verification pattern when enabling/disabling homepage popups.
- See `references/live-uvicorn-route-verification.md` for the stale-server / venv-import route verification pattern.
- See `references/ksr888-registration-game-buttons.md` for KSR888 GameXaGlobal player creation, local DB sync, lobby redirects, and always-visible game play buttons.
- See `references/ksr888-mobile-homepage-game-selection.md` for mobile homepage ordering and 1-game-per-active-provider selection in GAME TERPOPULAR.
- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs
- See `references/ksr888-game-launch-troubleshooting.md` for the KSR888 pattern where mobile routing is correct but provider launch still fails upstream.
- **Local binary pitfalls:** when a test runner/webServer command says a tool is missing, prefer `./node_modules/.bin/<tool>` over assuming a global install or PATH inheritance.
- **Virtualenv import pitfall:** if importing `backend.main` fails under system Python because a dependency like `httpx` is missing, use the repository virtualenv interpreter (`./.venv/bin/python`) for route inspection and app-level checks. If no repo venv exists, treat the import failure as an environment issue rather than a code defect until dependencies are verified.
- **Separate-process pitfall:** on shared dev hosts, a listening port may belong to a different assistant/bridge process. Confirm the PID and full command with `ss -ltnp` and `ps -fp <pid>` before assuming your app is running. Example: port 3000 may be a Hermes WhatsApp bridge while the ASPRI app runs elsewhere (e.g. 8090).
- **Stale-server pitfall:** if a live endpoint returns 404 but `app.routes` shows the path exists, check for an older process still bound to the port before changing code. Confirm the PID on the port, then restart that specific server instance and re-test. See `references/live-uvicorn-route-verification.md`.
- **Media output pitfall:** if `ffmpeg` output looks fine but is silent, inspect streams with `ffprobe` and confirm the pipeline actually mapped or generated audio. Existing output files should be regenerated if they lack an audio stream. See `references/video-audio-pipeline.md`.
- **yt-dlp subtitle fallback pitfall:** subtitle fetches can hit 429 or anti-bot errors even when the main video is reachable. If subtitles are optional, isolate them from the clip success path so the job can still complete. See `references/clipper-subtitle-429-fallback.md`.
- **yt-dlp anti-bot/runtime pitfall:** when yt-dlp warns about missing JS runtime or YouTube bot checks, centralize `--js-runtimes node:/usr/bin/node` and cookie-file support in one helper, and store Netscape cookies in the app data volume. See `references/youtube-antibot-yt-dlp.md`.
- **SSH-backed file access pitfall:** if `search_files`, `read_file`, or `terminal` fail with `SSH connection failed`, `Identity file ... not accessible`, or `Permission denied (publickey,password)`, treat it as an environment/access problem first. Do not keep retrying the same file query; verify SSH/config prerequisites, then fall back to `session_search` for known paths or ask the user to upload/provide the file path directly. See `references/ssh-file-access-failure.md`.


### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow systematic-debugging skill:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### With test-driven-development

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**
