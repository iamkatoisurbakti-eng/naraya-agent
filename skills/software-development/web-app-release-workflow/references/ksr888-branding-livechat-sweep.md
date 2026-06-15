# KSR888 branding + live chat sweep

## When to use
Use this note when an imported PHP host needs a domain-wide brand rename and a live-chat/Telegram swap on the live production site.

## What worked in this session
- User requested a full live-domain sweep: replace every visible `JP88` label with `KSR888` and replace all live chat / Telegram contact entry points with `KSR888BOT`.
- The repo had customer-facing strings in several places, not just one template:
  - `resources/views/layouts/main/master.blade.php`
  - `resources/views/layouts/main/main.blade.php`
  - `resources/views/layouts/desktop/prof.blade.php`
  - `resources/views/welcome.blade.php`
  - `resources/views/contact-us.blade.php`
  - `resources/views/layouts/maintenance.blade.php`
  - `rtp.php`
  - `mobile/index.php`
  - `dekstop/index.php`
  - `dekstop/template/nav.php`
  - `backoffice/template/page/contact/contact.php`
  - legacy provider scripts under `public/getprovider.php` and `public/getgame.php`
- After patching source, the live PHP container still needed explicit cache clearing and file sync.

## Pitfalls
- A source-level grep alone can miss stale strings because Laravel compiled views live under `storage/framework/views` and the running container may still serve cached HTML.
- `php artisan optimize:clear` inside the PHP container failed without a PTY in this environment with `Symfony\Component\Console\Exception\InvalidArgumentException: The StreamOutput class needs a stream as its first argument.`
- The fix was to run the command with an interactive PTY through `docker compose exec ksr888-web sh -lc 'cd /var/www/html && php artisan optimize:clear'`.
- Live HTML verification initially still showed old `Obrolan Langsung` / `LiveChat` text until the container-side sync and cache clear were done.
- Imported PHP hosts can also keep old brand/chat text inside runtime view-cache and old helper assets even when source files are already patched.

## Verification pattern
1. Search source and runtime for brand/chat strings:
   - `JP88`
   - `jp88provider`
   - `LiveChat`
   - `Livechat`
   - `Obrolan Langsung`
   - `livechatinc`
   - `lc.chat`
   - `tawk.to`
2. Patch both user-facing templates and contact/admin surfaces.
3. Copy the updated files into the running PHP container if needed.
4. Clear Laravel caches in-container with PTY.
5. Re-fetch the live page with a cache-busting query and confirm the old strings are gone.

## Files that commonly need a sweep
- `resources/views/layouts/main/master.blade.php`
- `resources/views/layouts/main/main.blade.php`
- `resources/views/layouts/desktop/prof.blade.php`
- `resources/views/welcome.blade.php`
- `resources/views/contact-us.blade.php`
- `resources/views/layouts/maintenance.blade.php`
- `backoffice/template/page/contact/contact.php`
- `mobile/index.php`
- `dekstop/index.php`
- `rtp.php`
- `public/getprovider.php`
- `public/getgame.php`

## Related workflow
- Imported PHP host release notes: `references/imported-php-host-release-notes.md`
- KSR888 auth/cache pitfalls: `references/ksr888-auth-login-register-logout.md`
- KSR888 DB/env + browser pitfalls: `references/ksr888-db-env-browser-and-category-strip.md`
