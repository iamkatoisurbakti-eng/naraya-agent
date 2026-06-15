# KSR888 admin setting section renames

Session notes for imported PHP host admin-panel cleanup.

## Goal
Keep the admin panel structure intact while renaming/reordering the visible section tabs in `Setting Website`.

## Section order used in this session
1. Info Website
2. Contact
3. Appearance
4. AutoGoPay QRIS
5. Setting Slider Banner
6. Setting Pop Up
7. Setting DP-WD
8. Setting API
9. Notifikasi

## Files touched
- `KSR888/site/resources/views/admin/setting/setting.blade.php`
- `KSR888/site/routes/web.php` (setting route already present for admin access)

## Pitfalls
- Do not change the underlying form payloads when the request is only about labels/order.
- Keep the tab ids and pane ids aligned when moving labels around.
- Rename the visible banner/popup cards too, not just the tab text, so the UI reads consistently.
- For imported PHP hosts, verify the live route after deploy with HTTP, since browser smoke can be blocked on this host.

## Verification
- Rebuild/deploy the PHP service.
- `curl -I https://ksr888.online/setting` should return the authenticated redirect when unauthenticated.
- After login, the Setting Website page should show the new section names in the requested order.
