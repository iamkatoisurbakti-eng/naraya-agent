# Landing promo 50% + full-frame hero/photo sync

Use this note when the user asks for a more full-screen photo/hero card or asks to add a promo CTA on the home page.

## What changed successfully in the session
- The landing hero CTA was changed to a stronger promo CTA (`AMBIL PROMO 50%`).
- The VIP/home pricing cards showed promo price + normal price side-by-side.
- Checkout/backend pricing was updated in the same change so the visible promo price and payable amount stayed consistent.
- Promo percentage was made env-driven (`PROMO_DISCOUNT_PERCENT=50`) instead of hardcoding the discount in scattered places.

## Practical implementation pattern
1. If the user wants the photo to feel more full-screen / fill the frame, adjust the media container, not just the image asset:
   - reduce inner padding
   - enlarge the hero/media zone
   - use `object-fit: cover` only for the specific card/section that must fill edge-to-edge
   - keep the subject centered and preserve any text safe-zone separately
2. If the user wants a promo on the home page, change both:
   - the visible hero/CTA copy
   - the pricing/checkout amount source of truth
3. Keep promo pricing customer-facing only:
   - show promo amount and normal amount/strike-through
   - do not expose internal margin math in public UI
4. Prefer env-driven campaign knobs for temporary promos so the same promo can be adjusted without another code sweep.

## Pitfalls
- Changing only the UI price while leaving checkout at the old amount creates a visible/paid price mismatch.
- Changing only checkout while leaving the home card unchanged makes the promo look fake.
- Do not overuse `cover` globally; use it only when the user explicitly wants the image to fill the frame more aggressively.

## Verification
- Rebuild the frontend after the copy/layout change.
- Re-check the built bundle for the promo CTA/price strings.
- If payment logic changed, smoke-check the quote/checkout calculation path so the displayed promo matches the payable amount.