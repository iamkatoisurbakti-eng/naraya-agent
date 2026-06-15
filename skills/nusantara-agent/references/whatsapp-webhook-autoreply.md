# WhatsApp inbound webhook autoreply

Session note for ASPRI Nusantara app.

Live inbound WhatsApp autoreply flow:
- GET /whatsapp/webhook and /whatsapp/webhook/verify are for Meta verification.
- POST /whatsapp/webhook is the inbound event receiver.
- When settings.enabled=true, inbound messages are parsed and replied to automatically.
- Replies are sent to the original sender number from the inbound payload, not a simulated test number.
- If message_id exists, the outbound reply uses reply_to_message_id to stay in thread.

Payload handling details:
- Normalize entry[].changes[].value.messages[].
- Extract text from:
  - text.body
  - interactive.button_reply.title / id
  - interactive.list_reply.title / id
  - button.text / payload
  - media captions for image/video/document/audio
- Ignore events without a sender or body.

Runtime requirements:
- WHATSAPP_PHONE_NUMBER_ID must be set.
- WHATSAPP_ACCESS_TOKEN must be set.
- Without those env vars, webhook still stores the inbound event but returns a dry-run/disabled reply result.

Storage behavior:
- Save the raw webhook event in whatsapp_events.json.
- Record inbound message in the session message log as status=received.
- Record outbound auto-reply in the same session log as status=sent.

Useful verification:
- POST a sample Meta webhook payload to /whatsapp/webhook.
- Confirm /bantu/whatsapp/config exposes webhook endpoints.
- Confirm /health remains OK after the webhook path is exercised.
