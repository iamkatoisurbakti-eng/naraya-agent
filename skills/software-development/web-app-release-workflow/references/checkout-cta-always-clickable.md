# Checkout CTA Always Clickable

Use this pattern when a checkout button looks broken to the user even though the UI state exists.

## Symptom
- User says the checkout button "doesn't work".
- The button may be visually present but disabled, or it may require a specific field state that is not obvious.

## Repro + diagnosis checklist
1. Open the live page in a real browser or JSDOM smoke.
2. Fill the minimum required field(s).
3. Check:
   - `button.disabled`
   - CTA class/state
   - helper/status text
   - modal/open action after click
4. If the CTA is disabled before input, confirm whether that is a product requirement or just a UI convenience.

## Preferred fix
- Keep the checkout CTA clickable by default when the page is meant to accept a click.
- Move the guard into `handleSubmit()` or the submit path.
- On empty required input:
  - show inline status text
  - focus the missing field
  - do not silently return
- After valid input:
  - update status text to a ready state
  - open the modal / continue the payment flow

## Regression test
- Add a unit test that proves:
  - checkout starts clickable
  - empty submit shows feedback and does not open the modal
  - filled submit opens the modal / payment flow
- Keep one live smoke that clicks the CTA after filling the minimum address field.

## Pitfall
- Disabling the button made the page feel broken and caused false reports that "the button cannot be used".
- For screenshot-matched checkout pages, the visible button state should usually stay active unless the reference explicitly shows a disabled CTA.
