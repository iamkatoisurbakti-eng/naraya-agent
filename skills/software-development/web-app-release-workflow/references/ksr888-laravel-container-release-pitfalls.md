# KSR888 Laravel Container Release Pitfalls

Session-specific deployment/verification notes for KSR888 Laravel app in Docker.

## Observed issue
`docker exec nusantara-ai-saas-ksr888-web-1 php artisan optimize:clear` can fail with:

```text
Symfony\Component\Console\Exception\InvalidArgumentException:
The StreamOutput class needs a stream as its first argument.
```

## Practical fallback
Use the app route already present in KSR888:

```bash
curl -sS -D - https://ksr888.online/clear-cache -o /tmp/ksr_clear.txt
cat /tmp/ksr_clear.txt
```

Expected body:

```text
DONE
```

Use normal TLS verification when possible. Only use insecure TLS flags if explicitly approved and needed for an environment issue.

## Container verification pattern
Host may not have PHP. Run checks inside the web container:

```bash
docker exec nusantara-ai-saas-ksr888-web-1 php -l app/Http/Controllers/backoffice/DatamemberController.php
docker exec nusantara-ai-saas-ksr888-web-1 php -l routes/web.php
docker exec nusantara-ai-saas-ksr888-web-1 php -l resources/views/admin/players/management.blade.php
```

For admin-only pages, unauthenticated HTTP probes should redirect. To verify rendering without exposing credentials, bootstrap Laravel inside the container with a synthetic request and `Auth::loginUsingId()` for an existing admin, then check for expected page strings.
