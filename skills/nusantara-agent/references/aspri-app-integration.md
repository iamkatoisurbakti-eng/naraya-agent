# ASPRI Nusantara App Integration Notes

Session outcome:
- ASPRI X Nusantara app now exposes a new feature key: `nusantara-agent`.
- Frontend home/chat surface is labeled `NUSANTARA AGENT`.
- Backend special-cases `feature == "nusantara-agent"` to call the local Nusantara API chat route directly.

Observed contract:
- `POST /feature/nusantara-agent` -> proxied to local Nusantara-Agent chat endpoint.
- `POST /workflow/run` with `feature=nusantara-agent` -> should use the Nusantara chat route and return a compact answer/steps/CTA payload.
- `GET /features` now includes a `nusantara-agent` entry.

Verification used in this session:
- `GET /health` -> 200
- `GET /features` -> included `nusantara-agent`
- `GET /workflow/templates?feature=nusantara-agent` -> 200
- `POST /feature/nusantara-agent` -> returned an answer from the local agent.

Pitfall:
- The app’s generic `/feature/{feature}` path may fall back to the Nusantara chat route only for this feature. Keep the special-case explicit so future refactors do not route it through a missing upstream feature handler.
