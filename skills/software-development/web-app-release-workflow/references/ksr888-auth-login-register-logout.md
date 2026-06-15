# KSR888 auth login/register/logout recovery

Use this note when login, register, or logout breaks on an imported PHP host like KSR888.

## Symptoms observed
- `GET /login` / `GET /register` returned `500` or redirected inconsistently.
- Register view crashed on `captcha_src('mini')` when the PHP `gd` extension was missing.
- Logout links sometimes pointed at `index.html` instead of a real logout route.
- Production URL generation could emit `http://` during redirects unless HTTPS was forced.

## Fix pattern
1. In the login controller, avoid rendering a missing `auth.login` view. If the host does not ship that view, redirect `/login` to the public entry page or the correct auth screen.
2. Keep admin and user login flows separate. If a user login succeeds but the account is admin-level, log out immediately and redirect to the admin login page.
3. Ensure the register view’s captcha driver is supported in the container:
   - install `gd`
   - verify with `php -m | grep -i '^gd$'`
4. If register uses `captcha_src('mini')`, remember the container must have the GD extension before the page can render.
5. Add an explicit `/logout` route and point all logout links to it.
6. In production, force HTTPS in the app service provider so redirect URLs do not bounce to `http://`.

## Verification
- `docker compose exec -T <php-service> php -m | grep -i '^gd$'`
- `curl -I https://<host>/login`
- `curl -I https://<host>/register`
- `curl -I https://<host>/logout`
- `curl -sS https://<host>/register | grep -n 'captcha/mini\|registerForm1\|logout'`

## Pitfalls
- A successful build does not guarantee the PHP container has the needed extension.
- A redirect to the site home can hide a missing login view instead of fixing the login form itself.
- Register pages can fail only at render time because captcha helpers are executed in Blade.
- If the host is behind a proxy/CDN, make sure the app forces HTTPS before judging auth redirects.
