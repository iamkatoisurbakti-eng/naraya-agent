# KSR888 game launch buttons on provider pages

Use this when a KSR888 provider page loads games but the user reports no `MAIN SEKARANG` button, especially on `/slots/server-b/{provider}/{type}`.

## Observed failure

- Desktop HTML may contain `MAIN SEKARANG`, but the button is hidden behind `.game-overlay` until hover or by CSS.
- Mobile (`@elsedesktop` branch in `resources/views/slots/games.blade.php`) can render only the image + game name, with no visible play button at all.
- Guest pages should still show a visible `MAIN SEKARANG` button that links to `/masuk`; logged-in pages should link to `/game_process/{game_code}/{game_provider}`.

## Fix pattern

1. Inspect `resources/views/slots/games.blade.php` separately for desktop (`@desktop`) and mobile (`@elsedesktop`) branches.
2. Desktop: if overlay exists but is not visible, add scoped CSS under `.sub-games #gamesContainer` to force `.game-overlay` and `.game_button_play` visible, clickable, and high contrast.
3. Mobile: add a small visible `<span class="mobile-play-now-btn">MAIN SEKARANG</span>` inside each game card.
4. Mobile logged-in card should use a real `href="{{ url('/game_process/' . $games->game_code . '/' . $games->game_provider) }}"` rather than duplicate `class` attributes plus `onClick` only.
5. Mobile guest card should use `href="{{ url('/masuk') }}"` and include the same visible button text.
6. Rebuild/recreate `ksr888-web`, then clear Blade/routes cache manually if `artisan` has TTY/ConsoleOutput issues.

## Verification

Use user-agent-specific live checks because desktop and mobile render different Blade branches:

- Mobile iPhone UA should show `MAIN SEKARANG`, `mobile-play-now-btn`, and guest `/masuk` links.
- Desktop UA should show `MAIN SEKARANG`, `game_button_play`, and forced overlay CSS.
- For authenticated launch verification, confirm logged-in HTML contains `/game_process/` links and click redirects into provider launch.

## Pitfalls

- A desktop curl can falsely pass while mobile is broken; always check both UAs.
- Counting `MAIN SEKARANG` in desktop HTML is not enough if CSS hides the overlay.
- Duplicate `class` attributes on an `<a>` can drop intended classes in browser parsing; merge them into one `class` attribute.
