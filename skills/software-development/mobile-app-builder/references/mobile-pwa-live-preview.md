# Mobile PWA Live Preview Pattern

Use this reference when the user asks for an Android/iOS app design and also wants to see it live immediately in Chrome.

## Pattern

- Treat the first deliverable as a responsive PWA/mobile web route when native store builds are not explicitly required for the same turn.
- Add a standalone mobile route such as `/mobile-app` or `/aspri-mobile` that renders a phone-frame UI at desktop widths and a full-screen mobile layout at handset widths.
- Keep the native app mental model: bottom/input safe area, touch targets >=44px, animated drawer/sidebar, conversation/history state, module switchers, and mobile viewport testing.
- If the app needs backend behavior, add a small API surface first (bootstrap/read state, chat/action mutation, module toggle/update). Persist simple prototype state in the app data directory, not in source.
- Deploy/restart the live web app so the user can inspect it in Chrome immediately; document source files and live URL in the final response.

## Verification

- Run the normal build/typecheck path for the repo.
- Verify the live route returns the SPA HTML: `fetch(URL).then(r => r.status)` or `curl -I`.
- Verify backend endpoints independently with JSON requests.
- If browser automation fails because of local Chrome/profile/snap issues, do not keep retrying the same browser call. Use available alternatives: direct HTTP checks, API probes, or a different browser executable/context.

## Pitfalls

- Do not claim a native Android/iOS binary was built if only a PWA/mobile web preview was delivered.
- Do not hardcode secrets into mobile/backend prototypes; use existing environment conventions.
- Avoid global CSS overrides that unintentionally neutralize the premium mobile route; scope route-specific button/gradient fixes under the route shell class.
