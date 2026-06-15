# Dashboard visitor privacy

Session-derived pattern for apps that track real visitor analytics but must not expose those metrics to normal users.

## Rule
- Real visitor/page-view analytics are admin-only operational metrics.
- Normal authenticated users should not see visitor cards, visitor labels, or visitor counts on their dashboard.
- Prefer replacing the user-facing card with an account-scoped metric such as `Generate Hari Ini`.

## Backend pattern
- Keep visitor analytics collection server-side (`visitor_events`) and admin endpoints intact.
- Do not send visitor keys from user dashboard APIs unless the authenticated user is admin.
- Example service signature:
  - `getDashboardSummary(userId, includeVisitorStats = false)`
  - normal `/api/dashboard/summary`: `includeVisitorStats = req.user.role === 'admin'`
- Omit these fields for non-admin users instead of returning zeros, so frontend/API consumers cannot infer operational traffic:
  - `visitorViewsToday`
  - `uniqueVisitorsToday`
  - `totalVisitorViews`
  - `uniqueVisitorsTotal`

## Frontend pattern
- Type visitor stats as optional.
- Render the visitor card only when `user.role === 'admin'`.
- For normal users, render a private/account-scoped replacement card such as today's generation count.

## Verification
- Register/login a temporary non-admin smoke user and call `/api/dashboard/summary`; assert visitor keys are absent.
- Create/sign an admin token or login admin safely; call the same summary route and assert visitor keys are present.
- Keep `/api/dashboard/admin/summary` protected by admin role and unchanged for admin panels.
- Clean live smoke users after verification.
