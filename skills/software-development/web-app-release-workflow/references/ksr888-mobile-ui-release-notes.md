# KSR888 mobile UI release notes

Use this as a condensed reference when changing KSR888 Blade/UI for responsive issues.

## Lessons from this session
- If a page shows on desktop but is blank on mobile, inspect the Blade structure first. A missing or malformed `@elsedesktop` block can leave mobile with no rendered content even when desktop is fine.
- Prefer a dedicated mobile section when the desktop layout is complex. For deposit, a separate mobile branch with its own heading, guide, form, and responsive spacing was clearer than trying to reuse the desktop markup.
- For fixed/sticky mobile buttons, default to removal unless explicitly needed. A sticky CTA can conflict with the bottom nav and make the page feel cluttered.
- If a user asks to hide an admin notification feature, remove the polling/toast logic entirely rather than just hiding the visible text.
- For popular-game sections, limit front rendering to GameXaGlobal records that have `game_image` populated from the API sync, and render mobile as a horizontal scroll-snap carousel when larger cards are requested.

## Verification notes
- Desktop and mobile must both be checked after Blade edits.
- If browser automation is flaky, verify the live page with `curl` plus a mobile user-agent and restart the web container after cache clear.

## Related files
- `resources/views/account/deposit.blade.php`
- `resources/views/layouts/desktop/gamerow.blade.php`
- `resources/views/admin/layouts/main.blade.php`
