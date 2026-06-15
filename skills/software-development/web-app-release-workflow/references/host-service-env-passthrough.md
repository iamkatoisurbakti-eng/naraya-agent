# Host service env passthrough for split PHP/Node stacks

When a repo serves multiple host types, the env vars must reach the service that *actually serves the route*.

## Lessons from this session
- If a PHP host is deployed as its own Compose service (for example `ksr888-web`), adding a feature such as Telegram notifications or payment callbacks must include env passthrough on that service, not only on the main Node app.
- A successful build of the main app does not prove the PHP host picked up the new env.
- Verify the target container directly:
  - inspect container env
  - confirm the expected variable is present
  - run a live smoke probe against the host-specific endpoint
- For notification flows, verify the real delivery target after deploy instead of assuming the code path is enough.

## Practical checks
- `docker inspect <service> | grep '<ENV_NAME>'`
- `docker compose ps`
- `curl` / browser hit on the live host route that should emit the notification
- if available, check the callback / delivery log in the host service rather than the main app
