# KSR888 sidebar audit and live GameXaGlobal counts

Use this when onboarding into KSR888 admin UI routes or when you need a live count of GameXaGlobal providers/games.

## Sidebar audit recipe
- Compare `routes/web.php` with `resources/views/admin/layouts/sidebar.blade.php` before editing menu labels.
- Check both admin branches and dev-only routes behind `dev_mode` middleware.
- After patching the sidebar, re-open the full file and verify there are no duplicate menu blocks or broken `@else` boundaries.
- Confirm active route matching (`Request::is(...)`) for the menu item you add.

## Live count recipe
- Read `gx_agent_code`, `gx_token`, and `gx_endpoint` from the KSR888 `api` table in the DB container.
- Use `curl` with `Authorization: Bearer <token>` to query:
  - `GET /api/games/providers`
  - `GET /api/games`
- Count providers from the root `providers` array or root `total` field.
- Count games from the root `total` field and cross-check the `games` array length.
- Use `jq` for deterministic counting; do not infer totals from a sample item.
