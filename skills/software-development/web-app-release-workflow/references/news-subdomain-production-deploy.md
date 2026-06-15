# News subdomain production deploy notes

Use this when deploying a public news site on `news.<domain>` from the same Docker Compose stack.

## Pattern used successfully
- Point DNS `news.nusantara-ai.online` to the VPS.
- Make the reverse proxy listen on both the apex domain and the news subdomain.
- Keep the app host-aware so the `news.` host opens the news-only surface.
- Allow both origins in backend CORS.

## Caddy / reverse proxy
- Update the Caddyfile host matcher to include both:
  - `{$DOMAIN}`
  - `news.{$DOMAIN}`
- After editing the Caddyfile, validate and restart Caddy:
  - `docker compose exec -T caddy caddy validate --config /etc/caddy/Caddyfile`
  - `docker compose restart caddy`
- If HTTPS returns a TLS alert on the new subdomain after a config change, do not assume DNS is wrong; restart Caddy first and retest.

## Verification
- `docker compose ps`
- `curl -kfsSI https://news.nusantara-ai.online/news`
- `curl -kfsSI https://nusantara-ai.online/`
- Confirm the response is `200` and that the news host serves the news route, not the dashboard shell.

## Pitfall
- A successful backend health endpoint does not prove the subdomain is live.
- The app can be healthy while Caddy is still serving stale config or stale TLS state.
- Always verify the public HTTPS host directly after restarting the proxy.
