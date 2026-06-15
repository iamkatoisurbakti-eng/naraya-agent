# MUI Class Mirroring for Screenshot-Matched Checkout

Use this pattern when the user points at a specific Material UI generated class string from a reference screenshot or copied DOM snippet.

## What to copy
- Preserve the exact wrapper class string on the matching element when it is part of the reference contract.
- Common examples:
  - `MuiTypography-root MuiTypography-h3 ...`
  - `MuiGridLegacy-root MuiGridLegacy-item MuiGridLegacy-grid-xs-true ...`
- Do not replace the exact class with a cleaner semantic class if the user explicitly asked for that class.

## What to pair with it
- Mirror the visual traits implied by the class:
  - typography weight/size/line-height
  - grid/flex behavior
  - spacing and alignment
- If the reference class is from MUI, the most important part is usually the rendered size/spacing rather than the library itself.

## Verification
- After patching, grep the source and the deployed HTML/bundle for the exact class string.
- If the page is static HTML, verify the class exists in live HTML after deploy.
- If the page is bundled, verify the class string survives the built bundle and the live page renders the same structure.

## Pitfalls
- Changing the class string to a lookalike and assuming the UI will match.
- Keeping the class name but forgetting the font/spacing rules that make it look right.
- Verifying only the source file and not the live deployment.
