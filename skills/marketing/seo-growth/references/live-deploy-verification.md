# Live deploy verification for SEO patches

Use this when a metadata/SEO change is patched in the source, but the public domain may still serve stale content.

Checklist:
1. Verify the source file changed in the repo/container build context.
2. Rebuild and restart the specific service that serves the public host.
3. Fetch the public URL with a cache-busting query string and a browser-like user agent.
4. Compare public HTML to the container-local HTML, not just one of them.
5. If the live site still shows old metadata, inspect proxy/CDN cache layers and the actual upstream service mapping.

Useful probes:
- curl -sS -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' 'https://example.com/?v=TIMESTAMP'
- docker compose exec -T <service> sh -lc 'curl -s http://127.0.0.1/ | head'
- docker compose ps --format json

Pitfalls:
- Rebuilding a container does not guarantee the public origin updated if the reverse proxy still points at an old service instance.
- A public domain can be cached separately from the container response.
- Always inspect the exact HTML source the search engine/browser would see.