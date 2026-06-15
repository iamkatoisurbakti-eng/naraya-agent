# KSR888 GameXaGlobal image sync runbook

Context:
- App path: /root/nusantara-ai-saas/KSR888/site
- Front should read provider/game images from local DB/cache, not hit GameXaGlobal during render.
- Image sync is done through `App\Services\GameXaImageSyncService::syncAll()` inside the web container.

Known-good execution pattern:
1. Run the sync inside the Laravel web container:
   `docker exec nusantara-ai-saas-ksr888-web-1 php artisan tinker --execute=' $r = app(App\\Services\\GameXaImageSyncService::class)->syncAll(); echo json_encode([...]); '`
2. Verify output includes provider/game counts and zero missing images when possible.
3. If front caches are stale, clear/rotate the cache keys used by the homepage, navbar, and provider catalog.
4. For repeated automation, wrap the command in a shell script under `~/.hermes/scripts/` and schedule it with `cronjob create`.

Pitfalls:
- Use the container’s PHP, not the host, if the host lacks `php`.
- `cronjob create` expects the script path relative to `~/.hermes/scripts/`.
- Keep secrets out of the script output; only print aggregate counts and status.
- After sync, reload/refresh the live site to confirm image URLs are served from DB/proxy routes.

Verification:
- `php -l` inside the web container for touched PHP files.
- `curl` the public page and confirm provider/game `<img src=...>` entries resolve through local proxy/storage URLs, not direct API render-time calls.
