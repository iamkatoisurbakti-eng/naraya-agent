# Checkout button activation regression

Use this when a checkout page looks fine but the primary CTA feels 'not working'.

## Symptom pattern
- Button click opens the modal, but the user thinks the button is broken because helper/status text does not change.
- The CTA is visually enabled, yet the page still shows stale guidance like `Alamat belum diisi.`.
- JSDOM or test builds may fail if a new UI test imports `jsdom` without a local declaration file.

## Root cause pattern
The activation logic only toggled the button state. It did not update the nearby status helper when the required field became valid.

## Minimal regression test
Write a unit test against the static checkout HTML that:
1. Loads `web/public/KSR.html` in JSDOM.
2. Confirms `checkoutBtn` starts disabled and `addrStatus` starts as `Alamat belum diisi.`.
3. Fills `addr1` and dispatches `input`.
4. Asserts:
   - `checkoutBtn.disabled === false`
   - `checkoutBtn.classList.contains('ready') === true`
   - `addrStatus.textContent === 'Alamat siap checkout.'`
5. Optionally clicks the button with fetch/QR stubs and asserts the modal opens.

## Build/test pitfall
If TypeScript build fails because a new test imports `jsdom`, add a local declaration file under `tests/unit/jsdom.d.ts` with:

```ts
declare module 'jsdom';
```

That keeps the production build green without pulling in extra type dependencies.

## Verification
- Run the targeted Jest test first.
- Then run `npm run test:unit`.
- Rebuild and redeploy the checkout page.
- Smoke-check the live page: type into `Baris 1 Alamat`, confirm the CTA enables, then click it and verify the QRIS modal appears.
