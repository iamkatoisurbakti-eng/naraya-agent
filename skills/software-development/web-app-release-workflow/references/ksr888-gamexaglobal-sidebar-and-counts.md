# KSR888 GameXaGlobal sidebar audits and live counts

Use this note when editing KSR888 admin sidebars/menu labels or when you need live GameXaGlobal provider/game totals.

## Sidebar/menu audit pattern
- Always compare `routes/web.php` with `resources/views/admin/layouts/sidebar.blade.php` before changing menu labels.
- Watch for split branches (`@if ($adminUser->level === 1)` vs `@else`) and dev-only routes behind `dev_mode` middleware.
- After patching the sidebar, re-read the whole file to ensure no duplicated blocks, broken `@else`, or moved menu items.
- Check active-state route expressions carefully; a wrong `Request::is(...)` can hide the current menu highlight even when the link is correct.

## Live GameXaGlobal counts pattern
- Read `gx_agent_code`, `gx_token`, and `gx_endpoint` from the `api` table in the KSR888 DB container.
- Use `curl` with `Authorization: Bearer <token>` against:
  - `GET /api/games/providers`
  - `GET /api/games`
- Provider totals may live in `providers` or `total` at the response root.
- Game totals may live in `total` at the response root, with the list in `games`.
- Use `jq` to count fields directly; do not guess from a sample item.

## Safe logging rule
- Never echo real tokens, secrets, or connection strings in chat or in generated files.
- If you need to display values in diagnostics, redact them in output text.
