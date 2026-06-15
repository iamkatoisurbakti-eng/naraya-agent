# Dashboard credit shape fallback

Session lesson: a full `npm run typecheck && npm run test` caught an e2e crash after login:

- Page showed ErrorBoundary: `Cannot read properties of undefined (reading 'toLocaleString')`
- Failing assertion waited for `Generations Hari Ini`, but the dashboard had already crashed.
- Root cause was a mock/legacy dashboard summary response with `credit: { used, limit }` while `DashboardPage` expected newer fields: `balance`, `lifetimePurchased`, `lifetimeUsed`.

Fix pattern:

```ts
type Credit = {
  balance?: number;
  lifetimePurchased?: number;
  lifetimeUsed?: number;
  used?: number;
  limit?: number;
};

const creditBalance = summary?.credit.balance ?? summary?.credit.limit ?? 0;
const lifetimeUsed = summary?.credit.lifetimeUsed ?? summary?.credit.used ?? 0;
const lifetimePurchased = summary?.credit.lifetimePurchased ?? summary?.credit.limit ?? creditBalance;
const creditProgress = summary
  ? Math.min(100, Math.round((creditBalance / Math.max(1, creditBalance + lifetimeUsed)) * 100))
  : 0;
```

Use normalized values in JSX:

```tsx
{summary ? creditBalance.toLocaleString('id-ID') : '...'}
{summary ? lifetimeUsed.toLocaleString('id-ID') : '...'}
{summary ? lifetimePurchased.toLocaleString('id-ID') : '...'}
```

Verification sequence used:

```bash
npm run test:e2e
npm run typecheck && npm run test && npm run test:live
bash scripts/deploy.sh
docker compose ps
curl -fsS https://nusantara-ai.online/api/health
```

If browser tool navigation hangs during live verification, use terminal Playwright smoke instead:

```bash
node --input-type=module <<'NODE'
import { chromium } from 'playwright';
const browser = await chromium.launch({ headless: true, executablePath: '/snap/bin/chromium', args: ['--no-sandbox'] });
const page = await browser.newPage();
const errors = [];
page.on('pageerror', err => errors.push(err.message));
page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
const response = await page.goto('https://nusantara-ai.online', { waitUntil: 'domcontentloaded', timeout: 30000 });
await page.getByText('KREASI TANPA').waitFor({ state: 'visible', timeout: 15000 });
await page.getByRole('button', { name: 'Masuk' }).waitFor({ state: 'visible', timeout: 15000 });
console.log(JSON.stringify({ status: response?.status(), title: await page.title(), errors }, null, 2));
await browser.close();
if (!response?.ok() || errors.length) process.exit(1);
NODE
```
