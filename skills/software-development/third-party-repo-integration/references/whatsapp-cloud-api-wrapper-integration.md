# WhatsApp Cloud API Wrapper integration notes

Source repo: https://github.com/fdciabdul/WhatsApp-Cloud-API-Wrapper

Session findings
- The upstream repo is a Node.js wrapper around Meta WhatsApp Cloud API, not a Python library.
- Core usage is thin: `Message` for send calls, `Media` for uploads/retrieval, `WebhookServer` for webhook parsing/verification.
- For a Python/FastAPI host app, map the SDK concepts to native HTTP endpoints instead of trying to embed the Node runtime.

Observed upstream shapes
- `Message(version, phoneNumberId, accessToken)` posts to `https://graph.facebook.com/{version}/{phoneNumberId}/messages`.
- `sendTextMessage(to, body, previewUrl=false)` uses `messaging_product=whatsapp`, `recipient_type=individual`, `type=text`.
- `Media(version, phoneNumberId, accessToken)` targets `/media` upload/retrieve endpoints.
- `WebhookServer` expects a GET verification callback and emits webhook payloads through an event emitter.

Host-app mapping used in ASPRI
- `GET /whatsapp/config` for capability/config visibility.
- `GET /whatsapp/webhook` and `POST /whatsapp/webhook` for Meta webhook verification + payload capture.
- `POST /whatsapp/messages/text|media|reaction|image|audio|document|video` for outbound sends.
- Incoming webhook payloads are normalized and stored locally for later admin review/automation.

Pitfalls
- FastAPI query params must use aliases for Meta verification keys: `hub.mode`, `hub.verify_token`, `hub.challenge`.
- If WhatsApp env vars are missing, return a dry-run/status response rather than pretending to send.
- Do not hardcode access tokens, phone number IDs, or app secrets in source or final responses.
- The vendor repo is reference material only; do not copy the Node runtime into a Python service.

Verification
- `python3 -m py_compile backend/main.py`
- Confirm webhook verification path returns the challenge text when the token matches.
