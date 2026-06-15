# KSR888 Admin Sidebar and Route Audit

Use this checklist when auditing admin menus/routes in KSR888-style Laravel apps:

- Check both admin branches separately. Some sidebars render different trees for level 1 admin vs developer/dev_mode users.
- Compare routes against `Request::is(...)` carefully; a wrong literal (for example, `sgx.providers` vs `other/providers`) breaks active states and can hide the menu highlight.
- When adding menu entries, keep route visibility aligned with middleware:
  - dev-only routes should stay out of the main admin menu if they require `dev_mode`
  - admin-safe routes can be grouped into a normal sidebar section
- When editing Blade sidebars, read the full file before patching. Partial-offset edits can accidentally duplicate blocks or shift `@else` boundaries.
- If a route exists but has no menu link, first decide whether it is intentionally hidden (dev-only) or simply missing from the sidebar.
- Good grouping pattern for admin finance/report pages:
  - History Play
  - Pengaturan Saldo
  - Bank
  - Transactions

Verification tips:
- Re-open the sidebar after each patch to ensure no duplicate blocks were introduced.
- Confirm the active menu state matches the actual route path.
- Make sure the final sidebar structure still has a single `@if / @else / @endif` nesting for the role-based branches.
