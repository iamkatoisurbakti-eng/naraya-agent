# Landing-page brand logo replacement notes

Context
- Session updated a React/Vite landing page that previously used placeholder model chips with initials and gradient boxes.
- Goal was to show more official-looking brand marks for model cards and keep the UI consistent.

Implementation pattern
- Prefer source edits in `web/src/...` and public assets in `web/public/...`.
- Define a small data object per card with:
  - `label`: visible model name
  - `brand`: token that maps to a known icon component
  - `tone`: fallback background classes for cards
  - optional `logoSrc`: root-relative public asset URL like `/brand-logos/minimax.svg`
  - optional `logoAlt`: explicit accessible alt text for image assets
- Avoid placeholder initials when the user asks for official/resmi model logos. Use `logoSrc` assets for brands missing from the icon library instead of leaving `SD`, `KL`, etc. in the UI.
- Render a reusable `ModelLogo` component that prefers `model.logoSrc` (`<img className="object-contain" />`) and falls back to the brand icon map only when no image asset is set.
- Keep full model/provider label text visible under the mark so brand marks do not become ambiguous.

Icon and asset availability notes
- `react-icons/si` can cover many official marks without adding image assets.
- Useful hits confirmed in this repo session:
  - `SiAnthropic`
  - `SiElevenlabs`
  - `SiFlux`
  - `SiGooglegemini`
  - `SiKuaishou` (good fallback for Kling/Kuaishou)
  - `SiOpenai`
  - `SiX`
- Previously used `SiBytedance` for Kling, but a more specific official mapping is `SiKuaishou` when available.
- `SiMinimax` was not exported by the installed `react-icons/si` package even though Simple Icons has a MiniMax slug; using a local `/brand-logos/minimax.svg` asset avoided the TypeScript failure.
- Simple Icons CDN may return 403 without a browser-like User-Agent. Retry downloads with `curl -A 'Mozilla/5.0' https://cdn.simpleicons.org/<slug>`.
- For missing exact icons, acceptable practical sources are official/static SVGs from Simple Icons CDN or provider favicons saved under `web/public/brand-logos/`.

Pitfalls
- Do not edit `web/dist/` for this kind of change; update source and rebuild.
- Do not assume a Simple Icons slug exists in the locally installed `react-icons/si`; probe exports with Node before importing, or typecheck immediately after adding imports.
- If a card has `logoSrc`, its `brand` may only be a type/fallback token; ensure the renderer actually prefers the image asset so the fallback icon is not shown.
- Re-run `npm run typecheck` after icon/data refactors; missing icon exports fail as TS import errors.
- After deploy, curl the public logo asset URLs and require HTTP 200 so Vite/public-path mistakes are caught.

Verification
- Run `npm run typecheck` and `npm run build:web` after the refactor.
- For deployed changes, run the project deploy script, curl `/api/health`, and curl each new `/brand-logos/...` asset path for HTTP 200.
