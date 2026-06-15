# KSR888 admin-panel feature addition without UI changes

## When to use
Use this note when adding a new admin dashboard feature on an imported PHP host like KSR888 and the user explicitly says not to change the default appearance.

## Pattern
- Keep the existing admin shell, sidebar, colors, spacing, and template structure intact.
- Add the feature by wiring only the minimum needed pieces:
  - route
  - controller method
  - data fetch / summary helper
  - admin menu item if needed
  - dedicated view that reuses the current panel layout
- Prefer placing new functionality inside an existing controller or nearby admin controller instead of introducing a second parallel flow with similar method names.
- Re-read the full controller file after patching to avoid duplicate method declarations; Laravel will fatal on redeclare and the live route may turn into HTTP 500.
- For a new admin page, verify both the route and the live response after deploy. If the page is behind auth, an HTTP 302 redirect to login is normal and not a failure.

## Verification
- Run `php -l` inside the live PHP container, not only on the host.
- Redeploy the host-specific web service after controller/route/view edits.
- Probe the exact live URL with `curl`.
- Confirm the page loads without visible layout changes unless the user explicitly asked for them.

## Pitfalls
- Duplicate controller methods can redeclare and break the page with HTTP 500.
- Auth middleware can make a healthy admin page look broken if you only check for 200 instead of the expected redirect.
- Editing build artifacts or mirror copies instead of the PHP source can leave the live site unchanged.
- UI-preserving requests should not be solved by redesigning the panel; keep the existing look and add only the missing feature surface.
