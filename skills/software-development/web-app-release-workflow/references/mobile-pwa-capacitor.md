# Mobile readiness for Nusantara AI (PWA + Capacitor)

## Goal
Make the existing web app usable on Android and iOS without rewriting the app in a separate mobile stack.

## Pattern used
1. Keep the React/Vite web app as the source of truth.
2. Add PWA support so the app can be installed from mobile browsers.
3. Add Capacitor packages so a native Android/iOS wrapper can be generated later.

## Files changed in this session
- `web/index.html`
  - added `manifest.webmanifest`
  - added favicon / apple touch icon links
- `web/public/manifest.webmanifest`
- `web/public/icons/icon.svg`
- `web/public/icons/icon-maskable.svg`

## Packages installed
- `@capacitor/core`
- `@capacitor/cli`
- `@capacitor/android`
- `@capacitor/ios`

## Verification
- Run `npm run build:web`
- Open the site on Android/iPhone and confirm it can be installed as a home-screen app

## Notes
- Do not replace the web app with a separate mobile rewrite unless the user explicitly asks.
- If the user asks for APK/IPA, continue from Capacitor rather than starting from scratch.
- Keep PWA icons and manifest under `web/public/` so Vite serves them correctly.
