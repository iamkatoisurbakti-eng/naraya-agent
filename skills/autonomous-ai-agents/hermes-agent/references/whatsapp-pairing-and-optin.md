# WhatsApp Pairing + Opt-in Guardrail

Use when a user asks to connect WhatsApp, scan a QR code, or send promotional WhatsApp messages through Hermes.

## Safety boundary
- Do not help with unsolicited WhatsApp blasting or scraped/cold target lists.
- First verify the target list is opt-in / previously consented.
- If not opt-in, offer safe alternatives: customer support bot, inbound auto-reply, opt-in campaign, draft templates, import workflow with consent fields.
- For opt-in promos, require messages to be polite, rate-limited, and include a STOP/unsubscribe instruction.

## Hermes WhatsApp setup workflow
1. Load `hermes-agent` skill before answering.
2. Check docs/CLI if needed: `hermes whatsapp --help`.
3. Start pairing with a PTY/background process:
   `hermes whatsapp`
4. If setup shows `Update allowed users? [y/N]`, press Enter unless the user asks to change allowed numbers.
5. If an existing session is found and the user wants a new barcode, ask before re-pairing because it clears the old session.
6. For re-pair: submit `y`, then read the process log and show the terminal QR to the user.
7. Tell the user to scan: WhatsApp/WhatsApp Business → Settings → Linked Devices → Link a Device.
8. After scan, poll the setup process and then start/restart gateway if needed.

## Notes
- Hermes stores WhatsApp session data under `~/.hermes/whatsapp/session` or platform session paths depending on version; treat it as sensitive credential material.
- Built-in Hermes WhatsApp uses a Baileys/WhatsApp Web bridge, not the official Business API; warn about account restriction risk for automation and prefer a dedicated bot number.
- Do not print or store WhatsApp session files in chat/log summaries.
