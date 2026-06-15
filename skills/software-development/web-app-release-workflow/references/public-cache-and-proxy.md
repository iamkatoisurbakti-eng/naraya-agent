# Public-site cache and proxy performance

For public web apps, first optimize cache headers and asset delivery before considering any proxy rotation.

What helped in this repo
- Serve hashed frontend assets with long-lived cache headers.
- Serve generated media with a shorter immutable cache window.
- Keep TLS/reverse proxy simple and stable; do not use rotate-proxy as a default speed fix for a public site.

Practical pattern
- Frontend static assets: `Cache-Control: public, max-age=31536000, immutable`
- Generated media: `Cache-Control: public, max-age=604800, immutable`
- Verify headers from the origin app, not only from the edge proxy.

When to use a CDN
- If the audience is geographically broad and asset latency remains high after caching.
- Prefer CDN/edge caching over rotating outbound proxies for user-facing pages.

Verification
- Check response headers for asset URLs.
- Confirm the public host still serves HTTPS correctly after deploy/restart.