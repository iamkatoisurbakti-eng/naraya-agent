# PHP AMP reference-page pattern

Use this when recreating an AMP landing page from a screenshot/reference URL on an imported PHP host.

## Pattern
- Create a host-specific PHP source file as the source of truth (for example `rtp.php`).
- Copy any referenced visuals into the host's local `assets/img/` directory instead of hotlinking remote images.
- Prefer a small, self-contained AMP layout with one hero banner, one CTA block, and one support table/grid.
- Keep copy short and high-contrast; AMP pages should read clearly on mobile first.

## Verification
- Run `php -l` inside the web container, not just on the host machine.
- Rebuild/restart the host service after editing the PHP source.
- Verify the rendered HTML with `curl`/`grep` against the live container or public host.
- If browser tooling is flaky, use HTTP + container verification instead of repeated browser retries.

## Pitfalls
- Remote hotlinked banners can fail or slow down the page later.
- AMP markup can look fine in source but still be broken if the container wasn't rebuilt.
- A visually similar page should still be brand-safe and original, not a verbatim clone of the source brand.