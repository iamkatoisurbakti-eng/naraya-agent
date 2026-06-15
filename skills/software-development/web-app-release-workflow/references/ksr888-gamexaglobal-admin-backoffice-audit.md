# KSR888 GameXaGlobal Admin/Backoffice Audit

Scope: admin/backoffice pages and controllers that still reference legacy provider labels or local provider-image fields after migrating catalog/source-of-truth to GameXaGlobal.

## Signals to inspect
- Admin titles that still say generic `Data Game`/`Data Provider` instead of the GameXaGlobal-backed source.
- Provider tables rendering old image fields such as `provider_background`, `mobile_provider_background`, or `provider_image` without the newer frontend accessors.
- Controllers that still branch on legacy provider names such as `fiver` or `PRAGMATIC`.
- Settings pages that expose local/provider-source terminology instead of the remote GameXaGlobal provider source.

## Files touched in this session
- `app/Http/Controllers/backoffice/GameAPIController.php`
- `resources/views/admin/games/provider.blade.php`
- `resources/views/admin/games/index.blade.php`
- `resources/views/admin/games/game_api.blade.php`
- `resources/views/admin/games/game_setting.blade.php`
- `resources/views/admin/component/updateProvider.blade.php`
- `resources/views/admin/component/updateOtProvider.blade.php`

## Patterns applied
- Provider list endpoint now reads from `gamexaglobal()->providers()` and returns normalized provider JSON.
- Table/image rendering prefers frontend accessors such as `frontend_banner_image`, `frontend_mobile_image`, and `frontend_provider_image`.
- Cache keys for provider/catalog data were version-bumped to avoid stale legacy payloads.
- Play links were aligned to the direct game process route instead of older provider-specific paths.

## Verification checklist
- Search admin/backoffice views and controllers for legacy provider names.
- Confirm admin tables and forms reference the same GameXaGlobal-backed fields exposed by the API/model accessors.
- Verify no hardcoded legacy provider labels remain in admin headings, breadcrumbs, or action modals.
- If PHP linting is unavailable in the environment, verify by source inspection and restart/deploy smoke checks instead.