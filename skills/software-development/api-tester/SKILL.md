---
name: api-tester
description: "Use when testing APIs for correctness, performance, auth behavior, payload shape, and error handling."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [api, testing, http, endpoints, auth, payloads]
    related_skills: [test-locally, evidence-collector, security-engineer]
---

# API Tester

Use this skill for API validation, endpoint discovery, auth probing, and response-contract checks. For session-specific endpoint maps and observed quirks, see `references/gamexaglobal-live-probe.md`.

## What this skill covers
- correctness of requests and responses
- auth behavior and token handling
- payload shape and schema drift
- error handling and failure modes
- performance and caching sanity checks
- endpoint discovery from docs, bundles, or client code

## Standard workflow
1. Discover the real live endpoint set first.
   - Check docs, bundles, routes, and client code.
   - Do not assume every documented route is actually wired.
2. Test auth boundaries explicitly.
   - Call protected endpoints without a token first.
   - Record exact `401/403/400` bodies before patching clients.
3. Verify happy path and failure path.
   - Exercise valid payloads, invalid payloads, and missing fields.
   - Compare live behavior to the expected contract.
4. Capture evidence.
   - Keep the raw status code, response body prefix, and any redirects.
   - Note unexpected off-domain redirects separately.
5. Only then patch client/server code.
   - Fix the root cause, not just the symptom.

## Live third-party / provider API probing
Use this when integrating a remote provider API into a product:
- enumerate all endpoints from the live JS bundle or API docs before coding
- probe login/auth endpoints with and without credentials
- confirm token type and header format before wiring helpers
- treat off-domain redirects or HTML responses as misrouted endpoints, not valid API contracts
- keep secrets redacted; never echo real tokens or passwords in logs or notes
- For provider APIs whose public docs/bundles expose a provider catalog, verify exact provider codes from `/providers` before calling provider-specific endpoints. Local/internal codes may not match upstream codes: on KSR888/GameXaGlobal, local Pragmatic `PR` returned `404 Provider not found`, while upstream codes were `PRAGMATIPLAY_SLOT` and `PRAGMATIC_LIVE_ASIA`.
- When the user provides a token in chat, use it only to update the runtime secret store/env/DB, then mask every verification output. If the token appeared in chat, recommend rotation after stabilizing integration.
- For provider catalogue/image ingestion tasks, do not stop at the broad `/api/games` endpoint. Fetch `/api/games/providers`, then each `/api/games/provider/{providerCode}` endpoint, normalize many possible image fields, fallback game images to provider artwork when needed, upsert by provider+game code, clear app catalogue caches, and verify DB image coverage. See `references/ksr888-gamexaglobal-game-image-sync.md`.
- For KSR888 slot/provider launch fixes, verify that local provider codes and local game slugs are translated to upstream GameXaGlobal provider codes and hash-like game IDs before calling `/api/games/launch`. Local `PR` + `vs20olympgold` can fail with `Game not found or inactive`; resolve via the live catalog and provider aliases first. See `references/ksr888-gamexaglobal-provider-auto-launch.md`.
- For KSR888 GameXaGlobal launch failures, do not assume local game codes are upstream launch codes. Legacy local codes such as Pragmatic `vs20olympgold` can list in UI but fail launch with `404 Game not found or inactive`; resolve local provider aliases (e.g. `PR`) and normalized game names against the live GameXaGlobal catalog before calling `/api/games/launch`. See `references/ksr888-gamexaglobal-slot-launch.md`.
- For KSR888 slot launch bugs, do not assume legacy card URLs (`/game_process/{oldGameCode}/{oldProvider}`) can be sent directly to GameXaGlobal. Map local provider aliases (e.g. `PR`) to upstream provider codes (e.g. `PRAGMATIPLAY_SLOT`) and resolve old game codes by normalized game name against the live catalogue before `/api/games/launch`. See `references/ksr888-gamexaglobal-slot-launch.md`.

## Checklist
- [ ] Endpoint is exercised
- [ ] Auth behavior is verified
- [ ] Errors are sensible and recorded
- [ ] Output matches contract
- [ ] Redirects and non-JSON responses are classified correctly
- [ ] Sensitive values are redacted

## Reference files
- `references/gamexaglobal-live-probe.md` — observed behavior and endpoint map for the KSR888/GameXaGlobal live probe, including transactions overview wiring, live stats payload keys, and Laravel container verification quirks
- `references/ksr888-gamexaglobal-game-image-sync.md` — KSR888 full provider/game image ingestion from GameXaGlobal, including provider-specific endpoint sweep, image field normalization, cache clearing, PTY script pitfall, and expected verification counts
- `references/ksr888-gamexaglobal-slot-launch.md` — KSR888 slot launch fix for mapping legacy provider/game card codes to GameXaGlobal live catalogue codes before `/api/games/launch`
- `references/ksr888-gamexaglobal-player-management.md` — KSR888 admin Player Management integration with GameXaGlobal players, local/provider mapping, balance sync, create-player flow, protected-route verification, and container cache-clear pitfall
- `references/ksr888-gamexaglobal-balance-sync.md` — KSR888 automatic user wallet sync verification for `/saldo-refresh`, admin `/update/saldo`, provider `players()+playerBalance()`, and Docker/Laravel route checks
- `references/ksr888-gamexaglobal-provider-auto-launch.md` — KSR888 provider-card auto-launch flow, local-to-GameXaGlobal provider/game-code aliasing, launch verification, and button-removal caveats
- `references/ksr888-gamexaglobal-slot-launch.md` — KSR888 slot launch debugging when local legacy provider/game codes fail against GameXaGlobal, provider alias/catalog-name resolution, and provider-card CTA button removal verification
