# KSR888 admin menu and modal audit

Use this when cleaning admin/backoffice labels and menus so the UI stays consistent with GameXaGlobal.

## Pattern
- Audit `resources/views/admin/layouts/sidebar.blade.php` first, then the relevant admin cards and modals.
- Check for route/label mismatches where the menu text says one thing but the active-state condition points elsewhere.
  - Example pattern: `URL::to('/other/providers')` should match `Request::is('other/providers')`, not an unrelated route fragment.
- Update modal copy in shared components such as `resources/views/admin/component/updateProvider.blade.php` and `updateOtProvider.blade.php` when provider naming changes.
- Re-check dashboard cards like `resources/views/admin/backoffice.blade.php` and API pages such as `resources/views/admin/games/game_api.blade.php` for old provider labels.

## Verification
- Search the admin tree for old provider labels and route fragments after patching.
- If the environment lacks `rg`, `python`, or `php`, fall back to `search_files` and `read_file`.
- If a file was read with pagination, re-read the full file before rewriting it to avoid clobbering unseen tail content.

## Common label cleanups
- Replace generic `Update Provider` titles with `Update Provider GameXaGlobal` when the modal is for GameXaGlobal data.
- Replace `Games List` / `Game API - All Provider` with `GameXaGlobal`-scoped wording when the page is backed by GameXaGlobal data.
- Keep status text explicit, e.g. `Live GameXaGlobal`, when the dashboard fetches GameXaGlobal data.
