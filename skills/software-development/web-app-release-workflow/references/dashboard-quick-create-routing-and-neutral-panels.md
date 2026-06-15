# Dashboard Quick Create routing and neutral panels

Use when improving the authenticated dashboard shortcuts or normalizing dashboard-only colored panels.

## Quick Create routing pattern
- Quick Create cards should be real actions, not inert buttons.
- Add an `onClick` prop to `QuickCard` and route to the matching dashboard section:
  - Image/logo 🖼️ -> `setActiveSection('images')`
  - Video/logo 🎥 -> `setActiveSection('video')`
  - Music/logo 🎵 -> `setActiveSection('music')`
  - Voice/logo 🎙️ -> `setActiveSection('voice')`
  - Clipper/logo ✂️ -> `setActiveSection('clipper')`
  - AI Chat/logo 💬 -> `setActiveSection('chat')`
- Keep the existing card layout/spacing intact; only add behavior.

## Neutral dashboard panel pattern
- If the user asks to remove purple/colored dashboard panels, scope the override to `.dashboard-shell` rather than changing global landing-page styles.
- Preserve layout, spacing, icon text, and feature logic. Override only backgrounds, gradient images, border colors, shadows, and broad accent text when needed.
- Use dashboard-scoped selectors for known Tailwind patterns such as `bg-gradient-*`, `bg-purple-*`, `bg-emerald-*`, `bg-sky-*`, `bg-rose-*`, `bg-fuchsia-*`, `bg-amber-*`, and similar.
- Do not remove status/error colors unless explicitly requested; status/error coloring helps UX.

## Verification
- Web-only dashboard UI changes: `npm run build:web && bash scripts/deploy.sh`.
- Fetch production health and the Vite JS/CSS bundles.
- Verify JS contains routing targets like `setActiveSection('images')`/compiled equivalents or the source built successfully.
- Verify CSS contains `.dashboard-shell` neutral panel overrides.
