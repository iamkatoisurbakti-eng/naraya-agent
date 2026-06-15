# KSR888 provider/game image DB sync

Session lesson: when syncing GameXaGlobal provider/game catalogs on the imported PHP host, persist image fields into the database so the homepage and category pages can read from DB instead of fetching remote API images on every request.

## What to store during sync
- `providers.provider_image`
- `providers.banner`
- `providers.mobile_banner`
- `games.game_image`

## Fallback rule
- Prefer the primary provider image from the API.
- If it is empty, fall back to `banner`, then `mobile_banner`.
- Do not blank existing DB image fields just because one API field is missing.

## Homepage rule
- Do not render a separate `PROVIDER API` section on the homepage if the requirement is only category-specific provider cards.
- Keep providers visible inside the category sections and let the homepage stay lean.

## Verification
- Run the sync and confirm DB rows contain non-empty provider image fields.
- Grep live HTML to ensure the `PROVIDER API` section is absent.
- Verify the live homepage still loads with HTTP 200 after cache clear and deploy.