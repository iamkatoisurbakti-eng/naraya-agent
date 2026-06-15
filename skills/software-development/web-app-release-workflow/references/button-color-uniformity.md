# Uniform transparent-white button color changes

Use when the user asks to make all buttons a single neutral color without changing the page layout.

## Pattern used
- Prefer a CSS override in the global stylesheet instead of editing every JSX button class when the request is color-only.
- Keep spacing, radius, typography, disabled opacity, and DOM structure intact; override only `background`, `background-image`, `border-color`, `color`, and optionally `box-shadow`.
- A safe selector for this React/Tailwind app was:
  ```css
  :where(button, .btn, a.btn, a[download], a.inline-flex.rounded-2xl) {
    background: rgba(255, 255, 255, 0.10) !important;
    background-image: none !important;
    border-color: rgba(255, 255, 255, 0.28) !important;
    color: #fff !important;
    box-shadow: none !important;
  }
  :where(button, .btn, a.btn, a[download], a.inline-flex.rounded-2xl):hover {
    background: rgba(255, 255, 255, 0.18) !important;
    background-image: none !important;
    color: #fff !important;
  }
  :where(button, .btn, a.btn, a[download], a.inline-flex.rounded-2xl):disabled {
    background: rgba(255, 255, 255, 0.06) !important;
    color: rgba(255, 255, 255, 0.60) !important;
  }
  ```

## Dashboard-only follow-up pattern
If the global homepage-style override is not affecting authenticated dashboard buttons consistently, add a stable wrapper class to the dashboard root and scope a second override there. This keeps the change button-only and avoids rewriting every Tailwind class:
```tsx
<div className="dashboard-shell flex min-h-screen ...">
```
```css
.dashboard-shell button,
.dashboard-shell a.inline-flex,
.dashboard-shell a[download] {
  background: rgba(255, 255, 255, 0.10) !important;
  background-image: none !important;
  border-color: rgba(255, 255, 255, 0.28) !important;
  color: #fff !important;
  box-shadow: none !important;
}
.dashboard-shell button:hover,
.dashboard-shell a.inline-flex:hover,
.dashboard-shell a[download]:hover {
  background: rgba(255, 255, 255, 0.18) !important;
  background-image: none !important;
  color: #fff !important;
}
.dashboard-shell button:disabled,
.dashboard-shell a.inline-flex:disabled,
.dashboard-shell a[download]:disabled {
  background: rgba(255, 255, 255, 0.06) !important;
  color: rgba(255, 255, 255, 0.60) !important;
}
```

## Dashboard panel follow-up
If the user broadens the request from button-only to “panel ungu/warna lain jadi transparan,” do not keep using the button-only selector. Use a separate dashboard-scoped panel reference (`references/dashboard-quick-create-routing-and-neutral-panels.md`) so future work does not accidentally flatten landing cards or text/icon colors.

## Verification
- Run `npm run build:web && bash scripts/deploy.sh` for web-only color changes.
- Verify public health and that the live CSS bundle contains the uniform button rule.
- For dashboard-scoped changes, also verify the live JS bundle contains `dashboard-shell` and the live CSS bundle contains `.dashboard-shell button`.
- Raw homepage HTML may not show button styles in a Vite SPA; fetch the linked `/assets/*.css` and `/assets/*.js` bundles and grep for the rule/marker.

## Pitfalls
- Do not rewrite card/status/badge colors when the user explicitly says “button saja”. Colorful badges/cards may remain unchanged.
- Global overrides with `!important` are useful here because Tailwind utility classes are spread across many components, but scope the selector to buttons and CTA-like links only.
