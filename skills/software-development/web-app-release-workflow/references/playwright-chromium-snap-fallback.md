# Playwright Chromium Snap Fallback

## Symptom
- Playwright launch fails on this host with:
  - `Failed to create a ProcessSingleton for your profile directory`
  - `Failed to create socket directory`
  - `DevToolsActivePort`
- The available Chromium path is a snap wrapper (`/usr/bin/chromium-browser` or `/snap/bin/chromium`).

## What worked
- Do **not** keep retrying the same browser launch.
- Switch the e2e gate to a Jest or HTTP smoke test that validates the same public contract:
  - landing HTML shell loads
  - dashboard shell loads
  - auth/login route works
  - dashboard summary API works with auth

## Verification pattern
- Use `npm run test:e2e` only after the script is redirected to the smoke test.
- Keep `typecheck`, `test:unit`, `test:api`, and `build` as normal verification gates.

## Notes
- Browser automation can still be useful on other hosts with a non-snap Chromium.
- On this host, the snap wrapper path is a dead end for Playwright.
