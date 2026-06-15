import fs from 'node:fs/promises';
import path from 'node:path';
import { chromium } from '@playwright/test';

function argValue(name, fallback = '') {
  const idx = process.argv.indexOf(name);
  if (idx >= 0 && process.argv[idx + 1] && !process.argv[idx + 1].startsWith('--')) return process.argv[idx + 1];
  const entry = process.argv.find((v) => v.startsWith(`${name}=`));
  return entry ? entry.slice(name.length + 1) : fallback;
}

function boolArg(name, fallback = false) {
  if (process.argv.includes(name)) return true;
  const v = argValue(name, '');
  if (!v) return fallback;
  return ['1', 'true', 'yes', 'y', 'on'].includes(v.toLowerCase());
}

async function renderOne(browser, htmlPath, outputPath, selector, waitMs) {
  const html = await fs.readFile(htmlPath, 'utf8');
  const width = Number(argValue('--width', htmlPath.includes('video') ? '1080' : '1080'));
  const height = Number(argValue('--height', htmlPath.includes('video') ? '1920' : '1350'));
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: Number(argValue('--scale', '1')) });
  await page.setContent(html, { waitUntil: 'domcontentloaded' });
  if (boolArg('--start-video', htmlPath.includes('video'))) {
    await page.evaluate(() => { if (typeof window.startVideo === 'function') window.startVideo(); });
  }
  if (waitMs > 0) await page.waitForTimeout(waitMs);
  const target = selector && selector !== 'full' ? page.locator(selector) : page;
  await target.screenshot({ path: outputPath, fullPage: selector === 'full' });
  await page.close();
}

async function main() {
  const input = argValue('--input');
  if (!input) throw new Error('Usage: node render-html-to-png.mjs --input <file-or-dir> [--output-dir <dir>] [--selector #slide]');
  const selector = argValue('--selector', 'full');
  const waitMs = Number(argValue('--wait-ms', '300'));
  const outputDir = argValue('--output-dir', '');
  const stat = await fs.stat(input);
  const htmlFiles = stat.isDirectory()
    ? (await fs.readdir(input)).filter((f) => f.endsWith('.html')).map((f) => path.join(input, f))
    : [input];

  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.PLAYWRIGHT_CHROMIUM_PATH || '/snap/bin/chromium',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  try {
    for (const htmlPath of htmlFiles) {
      const outPath = outputDir
        ? path.join(outputDir, path.basename(htmlPath).replace(/\.html$/, '.png'))
        : htmlPath.replace(/\.html$/, '.png');
      await fs.mkdir(path.dirname(outPath), { recursive: true });
      await renderOne(browser, htmlPath, outPath, selector, waitMs);
      console.log(JSON.stringify({ htmlPath, outPath }));
    }
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : String(error));
  process.exit(1);
});
