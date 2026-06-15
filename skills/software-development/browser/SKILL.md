---
name: browser
description: "Use when interacting with a live website in a browser for inspection, QA, navigation, form filling, or visual verification."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [browser, web, qa, verification, navigation, forms, visual-inspection]
    related_skills: [dogfood, web-app-release-workflow, debugging-hermes-tui-commands]
---

# Browser

## Overview

Use this skill when the task requires a live browser session to inspect, interact with, or verify a web page.

## When to Use

Use when you need to:

- navigate a website interactively
- click buttons, menus, or links
- fill forms and submit data
- inspect rendered page state
- verify layouts, screenshots, or UI behavior
- debug client-side or browser-only issues

## Working Style

1. Load the page and inspect the live DOM/state.
2. Refresh snapshots after interactions.
3. Prefer direct browser actions over assumptions.
4. Use visual inspection for layout-heavy or image-heavy pages.
5. Verify the end result after each meaningful change.

## Common Pitfalls

- Relying on static page source when the page is dynamic.
- Missing state changes that only appear after interaction.
- Forgetting to refresh snapshots after clicks or typing.
- Treating a screenshot as enough when DOM inspection is needed.
- If browser auto-launch fails because Chrome/profile/socket state is already in use, fall back to a fresh browser profile or non-browser verification. On shared hosts, Chromium may fail with a ProcessSingleton/profile-directory error even when no visible browser is open; in that case use terminal-side HTTP checks or launch with an isolated user-data dir instead of retrying the same browser session. For deployed React/Vite pages, verify both local and public URLs with `curl --compressed`, confirm the HTML references the new `/assets/*.js`, and clearly label browser automation as environment-blocked rather than app-failed.
- For responsive bugs, verify the live page with a mobile user-agent in addition to desktop rendering. Also check fixed/sticky elements against the mobile bottom bar and test horizontal scroll-snap carousels by swiping, not just by clicking arrows.

## Verification Checklist

- [ ] The live page was loaded
- [ ] The relevant elements were inspected
- [ ] Interactions were performed in-browser
- [ ] The final state was verified
