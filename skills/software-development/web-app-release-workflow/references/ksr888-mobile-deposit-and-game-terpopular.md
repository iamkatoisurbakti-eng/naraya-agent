# KSR888 mobile deposit and GameXaGlobal terpopular front

Use this reference when fixing KSR888 mobile deposit pages or the front-page "GAME TERPOPULAR" section.

## Mobile deposit rule
- If a Blade template uses `@desktop` / `@elsedesktop`, mobile must have its own fully rendered branch.
- Do not assume content wrapped in the desktop branch will appear on phones.
- For deposit pages, prefer a simple mobile card with visible nominal input, quick amounts, and a normal submit button.
- Avoid hiding the only usable action behind a sticky overlay unless the user explicitly wants it; in this session the sticky "Deposit Cepat" CTA was removed after the user asked.
- When the desktop branch renders deposit correctly but mobile is empty, check for a missing standalone `@elsedesktop` branch instead of tweaking desktop CSS.

## Game TERPOPULAR rule
- Source the cards only from DB rows that are synced from GameXaGlobal.
- Require a non-empty `game_image` and filter to `game_api = gamexaglobal` or `providerapi = gamexaglobal`.
- Use the model/accessor image URLs or proxy routes; do not mix in legacy providers without API-backed images.
- Keep the style responsive: grid cards on desktop, 2-column cards on mobile.

## Verification
- Check live HTML with a mobile user-agent when browser tooling is unavailable.
- Confirm the section renders on both desktop and mobile views.
- After Blade changes, clear view cache and app cache, then restart the web container.
