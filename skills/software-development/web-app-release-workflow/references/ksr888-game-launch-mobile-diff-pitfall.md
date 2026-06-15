# KSR888 mobile game-launch diff pitfall

Context
- During a live KSR888 mobile launch fix, the failure was not in the Blade view itself but in the controller path that prepared the sorted game list.
- The mobile page returned 200 after the fix, but before that the controller could abort rendering because `Collection::diff()` was applied to Eloquent/stdClass rows.

Observed failure
- Error class: object-to-string conversion / collection diff on object items.
- Problem line: top-game sorting used `$game->diff($topGames)`.
- Symptom: the mobile game page/launch route failed before the play button could be used.

Fix pattern
1. Build a stable identifier list from the top subset, preferably `game_code`.
2. Remove duplicates with `reject()` or `filter()` against that identifier list.
3. Merge the top subset back with the remainder.
4. Verify the live mobile route with a mobile user-agent curl after deploy/restart.

Example pattern
- Good: `$topGameCodes = $topGames->pluck('game_code')->filter()->map(fn ($code) => (string) $code)->all();`
- Good: `$otherGames = $game->reject(fn ($item) => in_array((string) data_get($item, 'game_code', ''), $topGameCodes, true));`
- Avoid: `$game->diff($topGames)` when the collection contains objects.

Verification
- Run `php -l` inside the running web container if host PHP is unavailable.
- Restart the KSR888 web container after copying the edited PHP file.
- `curl -A 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) ...' https://ksr888.online/...` and confirm HTTP 200 plus the expected game markup.
