# Checkout address validation and clickability

## What happened
In the KSR checkout page, a disabled `Checkout` button made the flow feel broken even when the address field was handled correctly.

## Lesson
For this class of static checkout page:
- Keep the primary checkout CTA clickable by default.
- Use helper text / status text to explain missing input.
- Reserve `disabled` only for real backend or loading states.
- If the product wants validation feedback, update the status label instead of blocking the click.

## Recommended verification
1. Render the page in JSDOM.
2. Assert the button is clickable at load.
3. Assert empty address shows `Alamat belum diisi.`.
4. Fill `addr1`, dispatch `input`, and assert:
   - button remains clickable
   - helper changes to `Alamat siap checkout.`
5. Click checkout and confirm the QRIS modal opens.

## Related pitfall
If you add a new JSDOM-based unit test in this repo, the Docker build may fail if TypeScript sees `jsdom` without declarations. Add a local ambient declaration such as `tests/unit/jsdom.d.ts`.
