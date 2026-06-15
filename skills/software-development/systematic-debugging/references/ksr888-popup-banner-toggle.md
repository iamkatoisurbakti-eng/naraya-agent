# KSR888 popup/banner toggle (live Laravel)

Use this when a user wants the homepage popup/banner disabled or enabled and the app is running in a Dockerized Laravel container.

## Key observations
- The homepage popup is controlled by `genral_settings.statusPopup` in the live DB.
- In `resources/views/welcome.blade.php`, the modal is only rendered when `statusPopup != 1` and a valid popup asset path exists.
- If the app is served through a proxy/CDN, a direct browser fetch to the domain may return 403 even when the container-local app is fine.

## Safe live procedure
1. Inspect current values from the running container, not the host.
   - Example: `docker exec -i <container> php artisan tinker --execute='...'`
2. To disable the popup, set `statusPopup = 1`.
3. Verify the rendered HTML from inside the container with a browser-like user agent.
   - Check that the actual modal markup (`id="welcomeModal"` / `id="midil"`) is absent.
   - Do not rely only on grep for the script that attempts to show the modal.
4. If the host lacks PHP, treat that as an environment limitation and use the container shell instead.

## Pitfalls
- `welcomeModal` may still appear in the page script even when the popup is disabled; confirm the modal container is missing.
- `statusPopup = 0` means active; `statusPopup = 1` means disabled.
- Root-domain HTTP checks can be misleading if the edge proxy blocks requests; verify against `127.0.0.1` inside the container when possible.
