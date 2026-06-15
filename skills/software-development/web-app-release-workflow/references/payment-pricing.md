# Payment pricing: API cost × 5

Session note from Nusantara AI SaaS:
- Customer-facing selling price is derived internally using `selling price = apiCost × 5` unless a private business override is explicitly configured.
- Persist base API/provider cost and multiplier only in private backend/database fields for accounting/admin use; never expose the formula publicly.

Backend pattern:
- Public `amount` = final customer-facing price only.
- Private order row fields may include `cost_amount` = API/provider cost and `selling_multiplier` = 5.
- Public plan/checkout/order payloads must not include `apiCost`, `costAmount`, `originalAmount`, `sellingMultiplier`, or any margin/formula fields.

UI/API privacy pattern:
- Never show API/provider cost, `× 5`, margin, multiplier, `originalAmount`, `apiCost`, or `sellingMultiplier` in public/customer-facing UI or API payloads.
- Keep the checkout CTA using the final customer-facing `amount` only.
- If a discount exists, apply it to the selling price, not the base cost, unless the product rules explicitly say otherwise.

Pitfalls:
- Do not let the frontend recompute pricing or multiplier; it should render backend `amount` only.
- Do not expose internal plan properties in public responses even if the TypeScript type still contains them from older versions.
- If plans change, update both the backend plan source and the billing UI copy together.
- For top-up tiers requested as final IDR ranges (for example Rp100K–Rp999K), encode the private `apiCost` values so `apiCost × 5` equals the desired public amount (e.g. 20,000→100,000; 59,800→299,000; 100,000→500,000; 199,800→999,000), then verify `/api/payments/plans` exposes only final amounts.

Verification:
- Build server + web, run API tests, deploy.
- Authenticated `/api/payments/plans` smoke should show only `id`, `name`, `credits`, `amount`, `currency`, `description`, `isFree`.
- Grep built frontend bundles for forbidden public strings/keys: `apiCost`, `costAmount`, `originalAmount`, `sellingMultiplier`, `modal API`, `Harga Jual`, `× 5`, `x 5`.
