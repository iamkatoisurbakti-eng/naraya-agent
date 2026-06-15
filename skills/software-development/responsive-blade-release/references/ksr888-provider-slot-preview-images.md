# KSR888 Provider Slot Preview Images

## When this applies
Use when the KSR888 homepage provider strip must show a provider card image, but the requested image should come from an active slot game image rather than from provider branding fields.

## Pattern learned
- Source provider preview images from active slot games (`game_type` in `SL` / `slot`).
- Prefer the first active slot game image found for each `provider_code`.
- Keep provider dedupe by normalized `provider_code`.
- If a slot preview image is missing, fallback only then to provider branding fields.
- Keep the same provider title/text, but swap the thumbnail source to the slot-game image.
- When changing selection logic, bump the cached homepage catalog key so old render data does not survive deploy.

## Implementation notes
- In `HomeController`, build a slot-only game collection and group it by `game_provider` / `provider_code`.
- Expose a `slotProviderPreviewMap` to the Blade partial.
- In `content/provider.blade.php`, assign `slot_preview_image` from the slot-game map first, then fallback to `frontend_mobile_image`, `frontend_provider_image`, and `frontend_banner_image`.
- Keep the `Provider GameXaGlobal` label unchanged so layout behavior stays stable.

## Verification
- Inspect rendered HTML and confirm provider card `src` values are the active slot-game images.
- Confirm the provider strip still renders after deploy/restart in the live container.
- Check that provider codes remain unique after dedupe.
