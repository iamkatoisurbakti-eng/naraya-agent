# Live user chat via SSE in Nusantara AI SaaS

Use this when adding authenticated realtime chat between users to the existing React + Express + SQLite app.

## Backend pattern
- Add a dedicated auth-protected router, e.g. `src/routes/live-chat.ts`, and mount it in `src/app.ts` under `/api/live-chat`.
- Keep room metadata explicit and small at first (for example a single `public` room) instead of inventing private-room UX before requested.
- Add a SQLite table through `initializeDatabase()`:
  - `live_chat_messages(id TEXT PRIMARY KEY, room_id TEXT NOT NULL, user_id TEXT NOT NULL, body TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)`
  - index `(room_id, created_at DESC)`
- REST endpoints:
  - `GET /api/live-chat/rooms` with `requireAuth`
  - `GET /api/live-chat/rooms/:roomId/messages` with `requireAuth`, bounded `limit`
  - `POST /api/live-chat/rooms/:roomId/messages` with `requireAuth`, trim/collapse whitespace, reject empty body, slice to 1000 chars
- Realtime endpoint:
  - `GET /api/live-chat/rooms/:roomId/stream?token=<accessToken>` because native `EventSource` cannot set `Authorization` headers.
  - Verify token manually with `verifyToken()`, load user with `getUserById()`, set `Content-Type: text/event-stream`, `Cache-Control: no-cache, no-transform`, `Connection: keep-alive`.
  - Send initial `ready` event with latest messages, broadcast future `message` events to in-memory clients for that room, and send heartbeat `ping` every ~25s.
  - Remove the client on request `close` and clear heartbeat.
- Pitfall: if fetching the latest message with `ORDER BY datetime(created_at) DESC, id DESC`, multiple inserts in the same second can return the wrong row. After insert, fetch by inserted `id` (`messageById(id)`) before broadcasting/responding.
- Pitfall: in Express 5 typings, `req.params.roomId` can be `string | string[]`; wrap with `String(...)`. If `req.user` typing is not globally augmented, cast locally: `(req as Request & { user: SafeUser }).user`.

## Frontend pattern
- Add a reusable dashboard panel (`LiveChatPanel.tsx`) and a separate dashboard section id (for example `live-chat`) so AI chat (`chat`) remains distinct.
- Load access token from Zustand session or `tokenStorage`; open stream with `new EventSource('/api/live-chat/rooms/public/stream?token=' + encodeURIComponent(token))`.
- On `ready`, merge server messages; on `message`, merge one message by id; sort by `createdAt` and cap to ~100 recent messages.
- Keep mobile safe: sidebar chip label `Chat Live`, page heading `Chat Live`, input placeholder like `Tulis pesan untuk pengguna lain...`, and full-width/stacked controls on narrow screens.
- Preserve existing e2e accessibility names for AI Chat (`aria-label="AI Chat"`) when adding a new live-chat button; use a distinct `aria-label="Chat Live Pengguna"` for the new feature.

## Tests and verification
- Add API tests that register two users, list rooms, have user A post a message, and have user B fetch it. Include unauthenticated `401` and long-message truncation tests.
- Run: `npm run typecheck`, `npm run test:api`, `npm run build:web`, `npm run build:server`, `npm run test:e2e`.
- Local SSE smoke can register two users, open `fetch()` to the stream endpoint, read `event: ready`, post a message with the other token, then read the message text from the stream.
- Live smoke should verify:
  - `/api/health` OK and Docker app healthy
  - rooms endpoint works with auth
  - SSE stream receives posted message
  - mobile Playwright 390x844 can open dashboard, click `Chat Live Pengguna`, send a message, see it, has no console/page errors, and no horizontal overflow.
- After live smoke, clean deterministic smoke users/messages from the Docker volume database with `docker compose exec -T app node ...`; host-side `data/nusantara-ai.db` may not be the active Docker volume DB.
