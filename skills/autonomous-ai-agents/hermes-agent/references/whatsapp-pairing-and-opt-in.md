# WhatsApp pairing + opt-in sending guard

Use this when a user asks to link WhatsApp Web/Baileys through Hermes and then send promotional messages.

## Safety boundary
- Do not help with blasting/spam or unsolicited outreach.
- Before setting up outbound promotion, confirm targets are opt-in or have explicitly agreed to receive promotional WhatsApp messages.
- Prefer compliant flows: opt-in list import, clear brand identity, human-readable message, STOP/unsubscribe option, low send rate, and logs.
- If targets are not opt-in, offer strategy, drafts, and inbound/customer-support setup only.

## Pairing workflow
1. Load `hermes-agent` skill.
2. Start pairing in a real PTY/background process:
   `COLUMNS=180 LINES=60 hermes whatsapp`
3. If prompted `Update allowed users? [y/N]`, usually press Enter unless the user gives a new allowlist.
4. If an existing session is found and the user wants a new barcode, confirm re-pair because it clears the old session; then answer `y`.
5. Show the QR directly in terminal text. Tell user to scan from:
   WhatsApp / WhatsApp Business -> Settings -> Linked Devices -> Link a Device.
6. Poll process for `connected` / `Pairing complete`; then start/restart gateway if needed.

## If user sees “Can’t link to this device”
- Kill the current pairing process and restart with a wide terminal (`COLUMNS=180 LINES=60 hermes whatsapp`) so QR is not wrapped/garbled.
- In WhatsApp, remove old linked devices named Hermes/unknown devices, update WhatsApp, restart phone, ensure stable network, wait a few minutes, then scan a fresh QR.
- Use a dedicated WhatsApp Business/bot number rather than a personal account when possible.
- If it continues failing, WhatsApp may be blocking the unofficial Baileys/Web session for that account; recommend the official WhatsApp Business Cloud API for stable promotional/customer messaging.

## Session/security notes
- Session directory grants account access; do not share or commit it.
- Hermes docs mention session persistence under `~/.hermes/platforms/whatsapp/session`, but the current bridge output may show `/root/.hermes/whatsapp/session`; trust the live setup output for the active path.
