# Laravel Production State Debugging Notes

Use this when a live Laravel site looks broken but the root cause may be data/state rather than code.

## What to check first
- Live app logs for the last 24h
- Database row(s) that drive the failing view
- Public storage contents and symlink/state
- Actual rendered HTML from the live endpoint

## Common failure patterns
- DB field contains sentinel `0` instead of a real relative path, so Blade renders `/storage/0`.
- Upload succeeded to `storage/app/public/...`, but the app reads from a different path contract.
- `public/storage` is a real directory or drifted copy instead of the expected symlink/state.
- An admin form uploads a file, but a separate save path overwrites the DB field with an empty/default value.

## Practical fixes
- Normalize stored media paths in the view/controller before building URLs.
- Treat sentinel values like `0`, `null`, or empty strings as “no asset.”
- If the configured asset is missing, optionally fall back to the newest valid file in the intended storage folder.
- Prefer `Storage::disk('public')->url($path)` for relative public-disk files.
- Keep the fallback scoped so it does not hide broken admin saves forever.

## Verification recipe
1. Query the live DB row directly.
2. Inspect `storage/app/public` and the public-facing asset path.
3. Curl the live homepage and search for broken `/storage/0` or other obvious bad paths.
4. Verify the rendered HTML on both desktop and mobile branches if the template is split.

## Notes from KSR888
- Popup rendering broke because `genral_settings.popup` was `0` even though a file existed in storage.
- A safe fallback to the latest valid file in `storage/post-images` restored visibility while keeping the admin upload path usable.
- Admin favicon references should use an actual present asset; missing `/Admin/image/...` paths surface as noisy 404s in production.