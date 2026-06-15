---
name: mobile-app-builder
description: "Use when building or iterating on mobile applications for iOS and Android, especially cross-platform app creation, screens, navigation, and release-ready verification."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mobile, app-builder, react-native, ios, android, expo, navigation, release]
    related_skills: [agent-spec-mobile-react-native, browser, test-locally, web-app-release-workflow]
---

# Mobile App Builder

## Overview

Use this skill when creating or improving a mobile app for iOS and Android.
It focuses on practical app building: screens, navigation, state, assets, testing, and release checks.

## When to Use

Use when you need to:

- build a new mobile app
- add or revise mobile screens
- implement navigation flows
- adapt UI for iOS and Android
- integrate APIs, storage, notifications, or media
- prepare a build for local/device verification

## Working Style

For this user, app-building and coding tasks should be executed as a Hermes multi-agent workflow for high-quality output: orchestrator, research, planning, implementation, quality, documentation, infrastructure, review, design, frontend/backend, and backtest where relevant.

1. Define the app goal, platform targets, and core flows.
2. If the user wants to see an Android/iOS-style app live immediately in Chrome, ship a responsive PWA/mobile web preview route first, then note whether native binaries are still outstanding. See `references/mobile-pwa-live-preview.md`.
3. Build the smallest usable screen or feature first.
4. Verify navigation and state transitions.
5. Test on the intended device/emulator path.
6. Check assets, permissions, and release readiness.

## Best Practices

- Keep screen logic small and focused.
- Separate UI, state, and data access.
- Handle platform differences intentionally.
- Optimize long lists and heavy images.
- Verify both happy path and failure states.

## Common Pitfalls

- Building too many screens before the core flow works.
- Ignoring platform-specific layout issues.
- Forgetting permissions, deep links, or back navigation.
- Skipping local verification before release.
- Repeatedly retrying a broken browser automation path; if Chrome/profile/snap or Playwright browser support fails, switch to HTTP/API verification or another executable/context and clearly state verification limits.
- Presenting a PWA/mobile web preview as a completed native Android/iOS binary.

## Verification Checklist

- [ ] App goal and target platforms are clear
- [ ] Core navigation works
- [ ] Screens render correctly on mobile
- [ ] Local build/test verification passed
- [ ] Release-related checks were reviewed
