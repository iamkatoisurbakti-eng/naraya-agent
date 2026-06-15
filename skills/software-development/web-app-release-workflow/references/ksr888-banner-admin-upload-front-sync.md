# KSR888 banner admin upload → front sync

## Scenario
Imported PHP host `ksr888.online` needed an admin banner upload feature that immediately fed the public homepage slider without changing the visible layout.

## Working pattern
- Use the existing `banner` model/table and admin controller.
- Store uploaded files under a public path that the PHP host serves directly, e.g. `public/storage/post-images`.
- Save the database path as a relative asset path like `post-images/<filename>` so `asset('storage/' . $item->gambar)` works on the front.
- Make uploaded files persistent across container rebuilds by mounting `site/public/storage` into the live PHP container.
- Keep the front homepage source of truth in the main controller (`HomeController`) and filter to active banners only.

## Good verification sequence
1. Syntax-check the controller(s) inside the container.
2. Rebuild/redeploy the PHP host.
3. Fetch the live homepage HTML and confirm it points to `/storage/post-images/...`.
4. Probe every newly-added image URL with cache busting and confirm `200 OK` plus the expected content type.
5. Check that the file exists in both source (`site/public/storage/post-images`) and running container (`/var/www/html/public/storage/post-images`).
6. Query the `banner` DB rows and confirm `status=1`, correct `gambar`, and expected `urutan`.

For local image-path ingestion, see `references/ksr888-homepage-banner-ingestion.md`.

## Pitfalls
- `store('post-images')` can land in a storage location that is not public-facing unless the host maps it correctly.
- If the upload path is only inside the container filesystem, the banner disappears after redeploy.
- If the front still shows hidden/inactive banners, make the controller query only active rows before rendering.
