---
name: laravel-admin-sidebar-route-audit
description: Audit and repair Laravel admin sidebars, menu trees, route visibility, and role-based navigation consistency.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [laravel, admin, sidebar, routes, navigation, blade, role-based-ui, menu-audit]
    related_skills: [web-app-release-workflow, codebase-onboarding-engineer, senior-developer]
---

# Laravel Admin Sidebar Route Audit

Use this skill when an app has a Laravel admin panel with role-based navigation, nested Blade sidebars, and routes that may or may not appear in the UI.

## When to use

Use when you need to:

- audit which admin routes are missing from the sidebar
- align sidebar labels with the real route paths
- preserve role-based visibility across admin vs developer branches
- add grouped menu sections for finance, reports, settings, or game/admin tools
- fix active menu highlighting or broken `Request::is(...)` checks
- clean up Blade menu structures after incremental patches

## Workflow

1. Map the route list first.
   - Compare `routes/web.php` against the sidebar tree.
   - Identify routes that are intentionally hidden vs accidentally omitted.

2. Separate branches by role.
   - Check each `@if / @else` branch independently.
   - Admin and developer menus often diverge; do not assume a link is visible in both.

3. Verify route strings exactly.
   - Confirm `URL::to(...)`, route names, and `Request::is(...)` patterns match the actual URL.
   - Small literal mismatches can break active states or hide the wrong menu item.

4. Add missing links in logical groups.
   - Group related routes into stable sections such as:
     - Game & Provider
     - Finance & Report
     - Member
     - Setting / Profile
   - Keep dev-only tools out of the main admin menu unless the route is meant for all admins.

5. Read the full sidebar before patching.
   - Blade sidebars are easy to break with partial edits.
   - Partial-offset edits can duplicate blocks, shift `@else` boundaries, or leave nested lists unbalanced.

6. Re-check the structure after each change.
   - Confirm there is still only one valid role branch structure.
   - Make sure menu groups open on the correct active routes.

## Common pitfalls

- Adding a menu link in the wrong role branch.
- Surfacing a dev-mode route in the normal admin menu.
- Using the wrong `Request::is(...)` path fragment.
- Forgetting to update active states after renaming the URL.
- Patching a Blade file by snippet only and accidentally duplicating existing blocks.

## Verification

- Compare the final sidebar against `routes/web.php`.
- Open the admin route and confirm the correct section expands.
- Check that hidden/dev-only routes remain hidden when intended.
- Validate that no duplicate menu groups were introduced.

## Reference

- See `references/ksr888-admin-sidebar-route-audit.md` for the KSR888-specific sidebar/route audit checklist, including role-based branches and `dev_mode` visibility.
