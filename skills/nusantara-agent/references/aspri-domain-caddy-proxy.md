# ASPRI custom domain via Nusantara AI Caddy

Use when connecting the ASPRI static app to a public subdomain such as `aspri.nusantara-ai.online`.

## Current live shape

- ASPRI source: `/root/nusantara-agent/aspri-nusantara-app`
- Frontend systemd service: `aspri-frontend` on host port `8091`
- Backend systemd service: `aspri-backend` on host port `8090`
- Public domain: `https://aspri.nusantara-ai.online`
- Reverse proxy: `/root/nusantara-ai-saas/Caddyfile` mounted into Docker container `nusantara-ai-saas-caddy-1`
- From inside the Caddy container, host services are reachable at `172.17.0.1:8091` and `172.17.0.1:8090`.

## Caddy pattern

Add an HTTP redirect block if needed:

```caddyfile
http://aspri.nusantara-ai.online {
  redir https://{host}{uri} permanent
}
```

Add the HTTPS site block:

```caddyfile
aspri.nusantara-ai.online {
  encode zstd gzip

  @aspri_backend path /chat /features /feature/* /workflow/* /admin/* /learning/* /business/* /keuangan/* /modul/* /bantu/* /pos/* /lacak/* /aspri-whatsapp/* /whatsapp/* /arenafinder/* /gold/* /news/* /datarakyat/*
  reverse_proxy @aspri_backend 172.17.0.1:8090

  reverse_proxy 172.17.0.1:8091
}
```

Validate and reload:

```bash
cd /root/nusantara-ai-saas
docker exec nusantara-ai-saas-caddy-1 caddy validate --config /etc/caddy/Caddyfile
docker exec nusantara-ai-saas-caddy-1 caddy reload --config /etc/caddy/Caddyfile
```

Caddy can obtain Let’s Encrypt certs through Cloudflare when HTTP-01 can reach the origin; TLS-ALPN may fail behind Cloudflare but HTTP-01 can still succeed.

## Frontend API base adjustment

In `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`, make `apiBase()` use same-origin for the custom domain so HTTPS pages do not call `:8090` directly:

```js
function apiBase() {
  const host = window.location.hostname || "76.13.197.168";
  if (host === 'aspri.nusantara-ai.online') return window.location.origin;
  return `${window.location.protocol}//${host}:8090`;
}
```

Then restart frontend:

```bash
systemctl restart aspri-frontend
```

## Verification

```bash
curl -fsS -I https://aspri.nusantara-ai.online | head -n 1
curl -fsS https://aspri.nusantara-ai.online/features | head -c 200
tmp=$(mktemp)
curl -fsS https://aspri.nusantara-ai.online/frontend/index.html -o "$tmp"
python3 - "$tmp" <<'PY'
from pathlib import Path
import sys
html=Path(sys.argv[1]).read_text()
checks={
 'aspri_html':'ASPRI' in html,
 'api_same_origin':"aspri.nusantara-ai.online') return window.location.origin" in html,
 'google_only':'Masuk dengan Google' in html and 'login-pin' not in html,
 'produk':'ASPRI PRODUK' in html,
 'dompet_removed':'Dompet' not in html,
}
for k,v in checks.items(): print(k, 'PASS' if v else 'FAIL')
PY
rm -f "$tmp"
systemctl is-active aspri-frontend aspri-backend
```

## Pitfalls

- Do not edit a non-existent `/etc/nginx`; production traffic here is handled by the Docker Caddy container.
- The Caddy container does not resolve `host.docker.internal`; use `172.17.0.1` for host services.
- `curl https://... | head` may emit `curl: (23)` when `head` closes early; use `-o tmpfile` for verification.
- If Cloudflare returns 525, check Caddy certificate acquisition logs and wait for HTTP-01 completion.
- Google-only login still requires a Google OAuth Web Client ID whose authorized JavaScript origin includes `https://aspri.nusantara-ai.online`.
