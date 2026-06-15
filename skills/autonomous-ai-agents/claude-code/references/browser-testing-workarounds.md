# Browser Testing Workarounds for Hermes Sessions

Use this when the built-in browser automation or Chromium profile collides with an existing process.

## Symptoms observed
- `Failed to create a ProcessSingleton for your profile directory`
- `Failed to create socket directory`
- Browser tool opens, but the session cannot reuse the default Chromium profile

## Recovery pattern
1. Do not keep retrying the same browser profile.
2. Run a standalone Playwright script from the terminal instead of the browser tool.
3. Point the script at a known Chromium executable when available.
4. Force isolated temp state:
   - `HOME=/tmp/<unique>`
   - `XDG_CONFIG_HOME=/tmp/<unique>`
   - `XDG_RUNTIME_DIR=/tmp/<unique>`
5. Create the temp dirs before launch.
6. Prefer a deterministic viewport and wait for `networkidle` before asserting UI state.
7. For live dashboard checks, verify the rendered DOM text directly and save a screenshot for later review.

## Minimal launch template
```bash
node - <<'NODE'
process.env.HOME = '/tmp/visible-home';
process.env.XDG_CONFIG_HOME = '/tmp/visible-config';
process.env.XDG_RUNTIME_DIR = '/tmp/visible-runtime';
const fs = require('fs');
fs.mkdirSync(process.env.HOME, { recursive: true });
fs.mkdirSync(process.env.XDG_CONFIG_HOME, { recursive: true });
fs.mkdirSync(process.env.XDG_RUNTIME_DIR, { recursive: true });
const { chromium } = require('playwright');
(async() => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/path/to/chrome',
    args: ['--no-sandbox']
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  await page.goto('https://example.com', { waitUntil: 'networkidle' });
  console.log(await page.locator('body').innerText());
  await browser.close();
})();
NODE
```

## Verification tips
- Check for exact UI strings, not just route success.
- Save screenshots to `/tmp/` for later inspection.
- If the site requires login, use a fresh test account and wait for the post-login URL before checking content.
