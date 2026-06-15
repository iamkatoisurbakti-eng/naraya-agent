# WhatsApp Cloud API Wrapper + FlowKirim compatibility notes

Session outcome:
- Vendor repo cloned: `vendor/WhatsApp-Cloud-API-Wrapper`
- Host app: Python FastAPI (`backend/main.py`), so the wrapper was used as a capability reference rather than copied as a runtime dependency.

What was mapped into the host app:
- Core WhatsApp Cloud API actions:
  - send text
  - send media (image/audio/document/video)
  - send reaction
  - webhook verification
  - webhook event parsing/storage
- FlowKirim-compatible REST surface:
  - `/api/health`
  - `/api/test-node-connection`
  - `/api/api-tokens` and `/api/api-tokens/generate`
  - `/api/whatsapp/sessions/*`
  - `/api/whatsapp/messages/text`
  - `/api/whatsapp/messages/media`
- Local persistence added for sessions, messages, contacts, and generated tokens using JSON files.

Important design choices:
- Keep secrets in env only:
  - `WHATSAPP_API_VERSION`
  - `WHATSAPP_PHONE_NUMBER_ID`
  - `WHATSAPP_ACCESS_TOKEN`
  - `WHATSAPP_VERIFY_TOKEN`
  - optional `WHATSAPP_BEARER_TOKEN`
- If Cloud API credentials are missing, the message send path falls back to a dry-run response instead of failing the whole app.
- Webhook verification should accept Meta-style query aliases (`hub.mode`, `hub.verify_token`, `hub.challenge`).
- FlowKirim docs use bearer auth on session/message routes; the host app should preserve that shape when the token env is configured.

Verification notes:
- `python3 -m py_compile backend/main.py` succeeded.
- Attempting to import the app in this environment hit a missing runtime dependency (`httpx`), so syntax-level verification was the stable check available here.

Pitfalls:
- Do not assume the vendor repo should be installed verbatim; map its capabilities into the existing stack.
- Do not hardcode tokens or echo live secrets in logs or responses.
- Keep FlowKirim-style path compatibility separate from the native WhatsApp Cloud API layer so future refactors can swap one side without breaking the other.
