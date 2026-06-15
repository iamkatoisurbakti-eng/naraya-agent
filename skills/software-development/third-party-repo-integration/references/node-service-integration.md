# Node service integration notes for vendor repos

Case studied: `Leuthra/cek-resi` for ASPRI LACAK PAKET.

What the repo is:
- Node/Hono service for tracking Indonesian shipping resi numbers.
- Files of interest: `README.md`, `package.json`, `index.js`, `function.js`, `manual.js`.

Observed integration workflow:
1. Clone vendor repo into an isolated vendor path.
2. Read README + `package.json` + entrypoint files.
3. Install dependencies with `npm install` before testing runtime endpoints.
4. Start the service and probe the health route first (`GET /`).
5. Probe the real lookup route next (`GET /cek-resi/:number`).
6. If the lookup route stalls or times out, keep the host app’s local fallback logic in place instead of assuming the vendor service is production-ready.

Vendor-specific quirk:
- The root endpoint responded successfully, but the lookup path timed out in this environment.
- The host integration should therefore call the vendor service opportunistically and fall back to local tracking generation when it fails.

Reusable mapping pattern:
- Vendor capability: external tracking lookup
- Nusantara/ASPRI equivalent: `/lacak/track` or `/paket/track`
- Use mode: adapt
- Integration surface: backend service + fallback logic
- Pitfall: do not replace an existing internal tracker unless the vendor lookup has been verified end-to-end.
