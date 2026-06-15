# Mapping playbook for external repos

## Fast inspection order
1. `README.md` / `CLAUDE.md` / `CONTRIBUTING.md`
2. `package.json` or manifest
3. main export entrypoint (`src/index.*`, `lib/index.*`)
4. core service/engine files
5. example scripts

## What to extract
- core capabilities
- required runtime/dependency shape
- public API surface
- example usage patterns
- repo-specific instructions

## Decision buckets
- Direct use: drop-in or nearly drop-in
- Adapt: useful logic, different interfaces or host-app boundaries
- Defer: not needed for MVP

## Nusantara-specific notes from this session
- Firecrawl is best treated as a scraping engine/reference for URL extraction and structured web data.
- Affiliate-management-system is best treated as a feature map for referral, commission, payment history, fraud, analytics, and payout workflows.
- Clone vendor code under `vendor/<repo-name>` so it stays isolated from first-party app code.
- Strong README claims should be verified against `src/index.*`, core engines, and examples before being repeated in the app plan.
