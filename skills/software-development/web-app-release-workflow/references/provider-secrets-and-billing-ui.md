# Provider secrets and billing UI notes

Use for Nusantara-style Dockerized React + Express apps when live AI provider keys and merchant/billing UI are part of a release.

## Secret handling pattern
- Store real provider keys only in `.env.production` / `.env` / runtime environment. Never hardcode in `src/`, `web/src/`, `docker-compose.yml`, or final responses.
- When updating env files from values the user provided, do not echo the values back. Tool output and final text should say only `KEY=set` / `KEY=missing`.
- `docker-compose.yml` must pass every required env var through to the app service; setting only `.env.production` is not enough if compose does not list it.
- Verification command should mask values, for example:
  ```bash
  docker compose exec -T app node -e "for (const k of ['GOOGLE_API_KEY','GEMINI_API_KEY','ELEVENLABS_API_KEY','FAL_KEY','FAL_API_KEY','KLING_ACCESS_KEY','KLING_SECRET_KEY','ANTHROPIC_API_KEY']) console.log(k+'='+(process.env[k]?'set':'missing'))"
  ```
- For Gemini support, accept both `GOOGLE_API_KEY` and `GEMINI_API_KEY` in config. A practical text endpoint is `https://generativelanguage.googleapis.com/v1beta/models/<model>:generateContent?key=<encoded key>`.
- For Claude, use `ANTHROPIC_API_KEY`; for FAL, pass both `FAL_KEY` and `FAL_API_KEY` if the code checks either; for ElevenLabs, `ELEVENLABS_API_KEY`; for Kling, keep access and secret separate (`KLING_ACCESS_KEY`, `KLING_SECRET_KEY`) and expose only configured status unless a real Kling implementation exists.

## Provider status endpoint
- Status endpoints must report booleans only, not secret values.
- Include newly configured providers in both `studios` capability booleans and provider-specific booleans.
- If a provider is configured but no real call implementation exists yet, report it separately (for example `kling: true`) without pretending FAL-backed video calls are Kling.

## Billing UI cleanup
- Do not expose internal margin/COGS formulas in customer UI unless explicitly requested.
- Remove labels like `Formula Harga`, `Modal ×`, `Harga modal API`, `Harga jual`, `Harga jual normal`, `Harga jual IDR dari modal API × 5`, and raw base-cost rows from plan cards, landing pricing sections, QRIS checkout modals, and payment history.
- If `baseCost`/`originalAmount` can be null/undefined from the API, never render `rupiah(plan.baseCost)` or `rupiah(payment.originalAmount)` directly; it can display `RpNaN` or expose internal price math.
- A good customer-facing billing card shows plan name, credits, final price, and checkout button only.

## Verification checklist
- Search source and built/public page for forbidden text: `Saldo Kredit Live`, `Formula Harga`, `Modal`, `Harga jual`, `Harga jual normal`, `Harga jual IDR`, `modal API`, `RpNaN`, `Tersimpan di database`, `× 5`.
- Run `npm run build:server && npm run build:web`.
- Deploy with the project script.
- Verify `/api/health`, `docker compose ps`, and masked env status inside the app container.
