# KSR888 Laravel live UI cleanup

Use this reference for KSR888 imported Laravel pages when a live UI element must be removed or split cleanly between desktop and mobile.

## What we learned in this session
- If desktop shows the deposit form but mobile is blank, check for a missing mobile branch (`@elsedesktop`) or a desktop-only section that never renders on mobile. The fix can be to create a dedicated mobile view branch instead of trying to force desktop markup to work everywhere.
- For mobile deposit, prefer a simple native form submit to `create-payment` over JS-heavy AJAX/QR generation flows unless the JS path is fully proven.
- If a sticky mobile CTA is distracting or unnecessary, remove it entirely rather than leaving hidden JS references behind.
- When removing banners/sliders from a Blade view, delete the section from the rendered template and verify the live HTML after `view:clear` + `cache:clear` + container restart.

## Live verification pattern
1. Edit the Blade file in source.
2. Copy or rebuild into the live container.
3. Clear Laravel view/cache inside the container.
4. Restart the web container.
5. Verify with `curl` that the served HTML no longer contains the removed slider/banner markup.

## Cache / route cleanup notes
- If Laravel reports a missing cache lock file path under `storage/framework/cache/data`, recreate the directory inside the running container and ensure it is writable.
- If `route:list` complains about a missing legacy controller class, add a thin compatibility controller or update the route to class-based syntax so route discovery succeeds.

## Related files
- `resources/views/welcome.blade.php`
- `resources/views/account/deposit.blade.php`
- `resources/views/layouts/main/main.blade.php`
- `resources/views/layouts/main/master.blade.php`
- `routes/api.php`
- `app/Http/Controllers/Api/SeamlesController.php`
