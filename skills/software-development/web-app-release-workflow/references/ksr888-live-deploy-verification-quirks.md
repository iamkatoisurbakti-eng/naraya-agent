# KSR888 live deploy verification quirks

Session learning from GameXaGlobal image DB sync on `ksr888.online`.

## Verification gotchas
- Plain `curl https://ksr888.online/` can return a small partial script-only response (~1 KB) because the imported PHP app behaves differently for curl user agents.
- Use a browser-like user agent for homepage verification:
  `curl -L -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/147 Safari/537.36' https://ksr888.online/`
- Expected healthy homepage evidence after deploy:
  - HTTP 200
  - title contains `KSR888 : Situs Gacor terbukti membayar`
  - large HTML body (~hundreds of KB)
  - many `<img>` tags
  - `/game-image-proxy?u=` appears for DB-backed remote images
- Probe a few proxy URLs directly and verify `200 image/*`.

## Container/CLI quirks
- `php artisan tinker --execute=...` can fail in this container with `StreamOutput class needs a stream as its first argument` under non-interactive `docker compose exec -T`.
- For deterministic DB counts, prefer a temporary standalone PHP/PDO script copied into the container, then delete it from host and container.
- `php ./vendor/bin/phpunit ...` works even when `./vendor/bin/phpunit` is not executable.

## Deploy/restart notes
- After rebuilding `ksr888-web`, run `docker compose up -d --force-recreate ksr888-web` in background and wait for completion.
- Caddy may log transient `lookup ksr888-web ... server misbehaving` during container recreation; verify again after the service is `Up`.

## Git/source-control note
- `/root/nusantara-ai-saas` on this host is not a git repository. Do not promise push/commit for KSR888 unless a repo/remote is discovered first.
