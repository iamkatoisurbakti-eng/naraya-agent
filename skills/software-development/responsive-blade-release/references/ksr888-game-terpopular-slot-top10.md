# KSR888 GAME TERPOPULAR: slot-only 10 top items

Use this note when the KSR888 homepage needs `GAME TERPOPULAR` to show exactly 10 slot games on both mobile and desktop.

## Working pattern
- Source the list from the controller, not from a separate mobile-only and desktop-only data source.
- Filter to slot games only: `game_type` values seen live are `slot` and `SL`.
- Prefer a hard cap of 10 items for `GAME TERPOPULAR`.
- Dedupe by `game_code` first, not `game_name`; duplicate names can still represent distinct games and should not collapse the list.
- Keep a Blade fallback that still filters missing images and slot-only games if the controller payload is incomplete.
- When the home catalog is cached, bump the cache key after changing selection logic so stale renders do not hide the update.

## Verification
- Mobile HTML: confirm the `id="game-list"` section contains 10 `<li>` items.
- Desktop HTML: confirm the desktop branch renders the same slot-only top-10 list if that branch is active.
- If the rendered count is 9, check for duplicate `game_name` values; the fix is usually to dedupe by `game_code`.

## Live note from KSR888
- A live slot list initially rendered only 9 items because two different games shared the same name (`Zorro`), and the Blade dedupe key was based on name.
- Switching the dedupe key to `game_code` restored the expected 10 items.
