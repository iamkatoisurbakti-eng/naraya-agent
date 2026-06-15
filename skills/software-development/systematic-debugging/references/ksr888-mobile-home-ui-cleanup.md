# KSR888 Mobile Home UI Cleanup

Use this when a user asks to remove, move, or reorder home-page UI on KSR888 mobile without breaking desktop.

Key findings from the session:
- Mobile home shell is rendered in `resources/views/layouts/main/main.blade.php`.
- On the home route, it can include `content.home_banner_slider`, `content.provider`, and `content.gameNew`.
- `GAME BARU` lived inside `resources/views/content/gameNew.blade.php` as the second slider block; removing only that block preserves `GAME TERPOPULAR`.
- When the user wants the banner slider under the progressive jackpot on mobile, the correct fix is:
  1) remove `@include('content.home_banner_slider')` from `resources/views/layouts/main/main.blade.php`
  2) insert `@include('content.home_banner_slider')` in `resources/views/welcome.blade.php` immediately after the jackpot block
  3) keep the provider/game sections below it
- Host edits are not automatically live-mounted; copy the edited Blade file into `nusantara-ai-saas-ksr888-web-1:/var/www/html/...` and restart the container.
- Verify with a mobile UA curl, then grep the HTML order.

Fast verification example:
```bash
python3 - <<'PY'
import urllib.request
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'}
html = urllib.request.urlopen(urllib.request.Request('https://ksr888.online/', headers=headers), timeout=30).read().decode('utf-8', 'ignore')
for needle in ['jackpot_amount', 'homeBannerCarousel', 'gx-banner-ticker', 'GAME TERPOPULAR']:
    print(needle, html.find(needle))
PY
```