# ASPRI BANTU WhatsApp Auto-Reply Notes

Use this reference when adding or verifying WhatsApp support in the ASPRI Nusantara app family.

## Observed contract

- Backend endpoints:
  - `GET /bantu/whatsapp/config`
  - `POST /bantu/whatsapp/connect`
  - `POST /bantu/whatsapp/autoreply`
- Live verification was done with `curl` against the running FastAPI service.
- The connect flow returned both a saved session object and a test message result.
- The autoreply flow returned the generated `reply_text` plus the send result payload.

## Working pattern

1. Read current config first.
   - Confirm the WhatsApp integration is enabled and inspect the active session fields.
2. Connect a session with a test recipient.
   - Use a dedicated session name for the integration being tested.
   - Keep bearer credentials in the `Authorization` header; do not hardcode or echo real secrets.
3. Simulate an inbound message.
   - Provide `from_number`, `inbound_message`, and optional `reply_text`/`reply_prefix`.
   - Verify the generated reply is sent successfully and that the returned payload includes the event record.
4. Restart and re-check live behavior after deploy.
   - If the app serves stale output, the backend likely needs a restart even when the code patch is correct.

## Pitfalls

- Do not assume the connect endpoint only stores config; it may also trigger a real test send.
- Do not expose raw token values in logs, chat output, or docs.
- Keep the endpoint contract stable if the frontend depends on the returned `session`, `test_message`, and `event` fields.
