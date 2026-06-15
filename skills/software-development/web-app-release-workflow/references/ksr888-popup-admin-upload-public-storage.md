# KSR888 admin popup upload and public-storage fix

Use this reference when the admin panel can upload a popup file but the homepage still shows no popup.

## Symptoms
- Admin upload succeeds, but frontend popup does not appear.
- `genral_settings.popup` stays `0` or otherwise holds no usable file path.
- The file may exist on disk, but not under the public storage path the Blade view can reach.

## Fix pattern
1. Confirm the admin form posts the file field as `popup` and the controller route is `update.popup`.
2. In `SettingController::updatePopup()`, store the upload with public visibility so the frontend can access it, e.g.:
   - `storePublicly('post-images', 'public')`
3. Keep the database field `popup` as the rendered path, not a boolean flag.
4. If the row still shows `popup = 0`, the upload path was not saved and the frontend cannot render the popup.
5. In the homepage Blade, guard the modal so it only opens when `setting.popup` contains a valid path.
6. Support both image and video popup assets if the admin allows both.

## Verification
- Inspect the active `genral_settings` row after upload; the popup field should change from `0` to a real path.
- Verify the file exists under public storage, not only in a private `storage/app/...` location.
- If `docker exec -i ... artisan tinker` misbehaves with Symfony stream errors, use a small PHP script inside the container for verification instead.
- Restart/redeploy the web container after code changes so the live Blade and controller changes take effect immediately.

## Related live note
- This pattern was observed on KSR888 while fixing a homepage popup that was uploaded from admin but never rendered on the frontend until the storage path was made public and the view was guarded against empty values.
