# Deploy port conflict notes

Use this when `docker compose up` or deploy fails with `failed to bind host port ...: address already in use`.

## What to check
- `docker ps` for existing containers already publishing the port
- `ss -ltnp | grep ':3000'` (or the target host port)
- `ps -fp <pid>` for any non-Docker process using the port

## Common Nusantara AI case
- Host port `3000` was occupied by the Hermes WhatsApp bridge process.
- Fix: make the app host port configurable, default to `3001`, and keep the container port at `3000`.

## Verification
- Re-run deploy after changing the host port.
- Confirm `docker compose ps` shows the app mapped to the new host port.
- Confirm `curl http://127.0.0.1:<host-port>/api/health` succeeds.
