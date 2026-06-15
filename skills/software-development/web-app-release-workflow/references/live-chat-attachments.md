# Live chat attachments: SSE + JSON data URL upload

Use when adding file attachments to an auth-protected live chat feature in a React + Express app that already streams messages via SSE.

## Backend pattern
- Keep the existing JSON message endpoint if the app already uses `express.json({ limit: '50mb' })`; accept an optional `attachment` object:
  - `name`: original filename for display only
  - `mimeType`: browser-provided MIME type
  - `dataUrl`: `data:<mime>;base64,<payload>`
- Validate attachment before inserting the message row:
  - reject invalid data URLs with `CHAT_ATTACHMENT_INVALID`
  - reject unsupported MIME types with `CHAT_ATTACHMENT_UNSUPPORTED`
  - reject empty files with `CHAT_ATTACHMENT_EMPTY`
  - reject files over the product limit (10 MB worked for chat) with `CHAT_ATTACHMENT_TOO_LARGE`
- Allow message body to be empty only if an attachment exists; otherwise keep `CHAT_MESSAGE_EMPTY`.
- Store a compact `attachment_json` column on the message row, not the file bytes.
- Add migration safety for existing DBs:
  - include `attachment_json TEXT` in `CREATE TABLE IF NOT EXISTS live_chat_messages`
  - call `addColumnIfMissing(db, 'live_chat_messages', 'attachment_json', 'TEXT')`
- Write files under a durable data folder outside web build output, e.g. `data/live-chat-assets/<roomId>/<messageId>/<attachmentId>.<ext>`.
- Serve files with Express static before the SPA fallback:
  - `app.use('/live-chat-assets', express.static(path.resolve(process.cwd(), 'data', 'live-chat-assets'), ...))`
- Broadcast the saved message (including attachment metadata/url) through the existing SSE `message` event.

## Safe attachment metadata
Recommended response shape:

```ts
type LiveChatAttachment = {
  id: string;
  name: string;
  mimeType: string;
  size: number;
  url: string;
  kind: 'image' | 'video' | 'audio' | 'file';
};
```

Supported MIME types used in production smoke:
- images: `image/jpeg`, `image/png`, `image/webp`, `image/gif`
- docs/text: `application/pdf`, `text/plain`, `text/csv`, `application/json`
- audio: `audio/mpeg`, `audio/mp4`, `audio/wav`
- video: `video/mp4`, `video/webm`

## Frontend pattern
- Add a hidden `<input type="file">` triggered by an `Attach File` button.
- Read the selected file with `FileReader.readAsDataURL`.
- Validate size and MIME on the client for immediate feedback, but keep server validation authoritative.
- Preview pending attachment before send and allow removal.
- Render sent attachments by `kind`:
  - image: `<img loading="lazy">`
  - video: `<video controls preload="metadata">`
  - audio: `<audio controls preload="metadata">`
  - file: link/download-style card
- Send `{ body, attachment }` to the existing message endpoint; preserve realtime SSE handling unchanged.

## Verification checklist
1. `npm run typecheck`
2. API test: message with `data:text/plain;base64,...` stores metadata and the returned URL serves the file content.
3. API test: `text/html` or another disallowed MIME returns `400` with `error.code === 'CHAT_ATTACHMENT_UNSUPPORTED'` (this app wraps errors under `error`).
4. `npm run build:web` and `npm run build:server`.
5. E2E smoke with mobile viewport 390x844:
   - set auth tokens in localStorage using the app's actual keys (`nusantara.accessToken`, `nusantara.refreshToken`, `nusantara.user` in this repo)
   - open dashboard, click the exact accessible sidebar button (`Chat Live Pengguna` if duplicate labels exist)
   - upload a small text file via `setInputFiles('input[type="file"]', ...)`
   - send and assert filename visible
   - assert console errors empty and no horizontal overflow
6. After production smoke tests, delete deterministic smoke users/messages and remove their files from `data/live-chat-assets`.

## Pitfalls from this repo
- Do not store attachments in `web/dist`; it is a build artifact and gets replaced on deploy.
- Do not rely on a generic `getByRole('button', { name: /Chat Live/i })` if the dashboard has both sidebar and quick-card labels; use the exact accessible name.
- When using a helper like `req(path, opts)`, avoid overwriting caller-provided headers with default JSON headers after spreading; merge headers explicitly so `Authorization` is preserved.
- The API error response shape is `{ error: { code, message, details } }`, not top-level `code`.
