# WhatsApp Cloud API Wrapper + FlowKirim compatibility notes

Session takeaway:
- The upstream `fdciabdul/WhatsApp-Cloud-API-Wrapper` is a Node.js wrapper around Meta WhatsApp Cloud API, but the host app here is FastAPI/Python. Do not transplant the Node runtime wholesale.
- Best fit is a compatibility layer in the host backend that exposes FlowKirim-style routes while keeping local JSON-backed state for sessions, tokens, messages, and contacts.
- Keep secrets in env vars only; use status/dry-run responses when WhatsApp Cloud env vars are missing.

Vendor capability → host mapping:
- Create/list session -> local session registry (`/api/whatsapp/sessions`)
- Session status/get/disconnect/delete -> local session JSON store
- Send text/media -> host `/api/whatsapp/messages/*` routes that can later forward to WhatsApp Cloud API
- Webhook verify + webhook ingest -> host GET/POST webhook routes
- API token generate/list/delete -> local token store for compatibility with docs/examples

FlowKirim-specific quirks observed in docs:
- Docs use `/api/whatsapp/...` and `/api/api-tokens...` paths.
- Several example requests include a bearer token requirement even when the docs say the service is unauthenticated.
- `messages/text` expects `{session_id,to,message}` and `messages/media` expects `{session_id,to,media_url,type,caption}`.
- `type` is constrained to image/audio/video/document in the docs; keep a narrow validator in the compatibility layer.

News-provider quirk from the same session:
- External news APIs may return 404 for valid-looking category/source combinations.
- `fetch_news_feed` should treat non-200 responses as soft failures and return a fallback digest instead of raising out of the request path.

Verification pattern:
- After wiring the compatibility layer, run a syntax check and a live smoke test against `/health` and the compatibility endpoints.
- Prefer a local fallback response over a hard crash whenever upstream provider shape or status is unstable.
