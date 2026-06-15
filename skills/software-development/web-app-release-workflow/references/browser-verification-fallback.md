# Browser verification fallback

Use this when Playwright/browser automation cannot launch because Chromium exits with ProcessSingleton/profile/socket errors.

Observed failure pattern:
- `Failed to create socket directory`
- `Failed to create a ProcessSingleton for your profile directory`
- `DevToolsActivePort` not written

Recommended fallback:
1. Do not keep retrying identical Chromium launches.
2. If needed, clear stale Chromium temp/profile directories under `/tmp/org.chromium.Chromium.*`.
3. Prefer terminal verification:
   - fetch the live HTML with a browser-like User-Agent
   - resolve the active JS bundle from the HTML
   - grep the bundle for the route-specific UI copy or API path you expect
4. For SPA routes like `/admin`, do not rely on the HTML title alone; it may still reflect the shell/landing page while the hydrated bundle contains the correct route.
5. If the route-specific UI is only visible after hydration, verify via bundle grep or a real browser run with a working executable path and a unique user-data directory.

Example terminal probe:

```bash
html=$(curl -fsS -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' https://example.com/admin)
bundle=$(printf '%s' "$html" | grep -oE '/assets/index-[^" ]+\.js' | head -n 1)
curl -fsS -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' "https://example.com${bundle}" | grep -nE 'Article Drafts|/api/admin/article-generator/drafts'
```
