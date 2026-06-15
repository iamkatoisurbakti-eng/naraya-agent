# Dashboard feature injection + service registration

Use this pattern when adding a new user-facing feature into the Nusantara AI dashboard (for example `Template`, `Evaluasi`, `Jasa`).

## Pattern
1. Add a dashboard card/quick-card that routes to a real section.
2. Extend the dashboard section union/state to include the new feature id.
3. Import and render a dedicated panel component in the main dashboard switch.
4. If the feature needs data persistence, add the backend route and DB table first, then wire the panel to the route.
5. Run a frontend production build (`npm run build:web`) and verify the new label exists in the built bundle.

## For `Jasa` / service registration
- Only allow legal services that can be promoted publicly.
- Require an explicit legal confirmation checkbox.
- Keep the catalog to clear, practical categories such as design, photography, digital marketing, consulting, training, cleaning, events, IT, transport, and beauty services.
- Save the user’s services with stable fields:
  - business name
  - service name
  - category
  - mode (online/offline/hybrid)
  - city
  - contact
  - description
  - optional website
  - legal confirmation

## Pitfalls
- Don’t add a card without a matching dashboard section; that creates dead UI.
- Don’t create a public-facing service catalog that implies illegal or unverified services are allowed.
- Don’t verify with source only; confirm the built UI after `npm run build:web`.
