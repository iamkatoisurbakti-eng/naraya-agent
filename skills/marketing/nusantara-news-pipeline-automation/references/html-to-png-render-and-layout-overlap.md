# HTML to PNG render for news flyers

Session note: 2026-05-08

## What worked
- Render `.html` flyer templates to PNG with Playwright/Chromium.
- Use exact viewport sizes:
  - Instagram flyer: `1080x1350` for 4:5
  - Shorts frame or preview: `1080x1920` for 9:16
- Verify output with `file` or `ffprobe`/image tools after render.

## Reliable pattern
```bash
node - <<'NODE'
const fs = require('fs/promises');
const { chromium } = require('@playwright/test');
(async()=>{
  const htmlPath = '/path/to/flyer.html';
  const outPath = '/path/to/flyer.png';
  const html = await fs.readFile(htmlPath, 'utf8');
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.PLAYWRIGHT_CHROMIUM_PATH || '/snap/bin/chromium',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await page.setContent(html, { waitUntil: 'domcontentloaded' });
  await page.screenshot({ path: outPath });
  await browser.close();
})();
NODE
```

## Pitfall discovered
- A flyer can *look* like the font is broken when the real issue is **headline/subheadline overlap** or cramped vertical spacing.
- In this session, the flyer font itself was fine; the layout needed more breathing room between:
  - headline
  - subheadline
  - points block

## Fix pattern
- Move the headline slightly up or down only if needed.
- Increase the gap before the subheadline.
- Push the accent line and points block lower when the headline is tall.
- Re-render and inspect the PNG visually before sending.

## Verification
- Confirm the rendered PNG is `1080x1350` for Instagram 4:5.
- Review the PNG visually after every layout tweak.
- If the result still feels cramped, reduce headline size slightly before touching the body copy.
