# Chromium HTML→PNG Fallback and Telegram Caption Verification

Session note for Nusantara-AI News automation.

## What worked

- In this environment, Playwright/browser navigation calls were unreliable for local `file://` HTML pages.
- The stable fallback was the system Chromium binary:

```bash
chromium-browser --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --virtual-time-budget=6000 \
  --window-size=1080,1350 \
  --screenshot='/path/to/output.png' 'file:///path/to/template.html'
```

- The snap Chromium build can emit DBus/AppArmor warnings on startup; treat those as non-fatal if the command exits `0` and writes the PNG.
- Verify output with `file` and, if needed, a second screenshot pass after template tweaks.

## Telegram delivery note

- `sendPhoto` can be used for the first delivery, then `editMessageCaption` is a reliable fallback if the caption needs to be normalized or corrected immediately after sending.
- Keep captions as plain text when possible.
- Always verify the Telegram API response JSON is `ok: true` for both calls before reporting success.

## Practical rule

If browser automation is flaky or unavailable, prefer:
1. Write the HTML locally.
2. Render via `chromium-browser --headless`.
3. Validate dimensions with `file`.
4. Send the rendered PNG to Telegram.
5. Use `editMessageCaption` only if the caption needs a post-send correction.
