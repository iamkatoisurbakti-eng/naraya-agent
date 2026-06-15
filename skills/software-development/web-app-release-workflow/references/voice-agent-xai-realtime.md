# Voice agent studio + xAI realtime notes

Use this reference when adding a realtime voice-agent panel to a Dockerized React + Express app.

## Feature shape
- Treat voice agents as `capability: 'voice'`, separate from `audio`/TTS.
- Update all layers together:
  - frontend model capability union (`text | image | video | audio | voice`)
  - studio section type and metadata
  - dashboard/sidebar navigation and page title logic
  - model catalog entry, e.g. `grok-voice-think-fast-1.0` / `Grok Voice Think Fast 1.0`
  - backend `Capability` union and `requireCapability`
  - generation route handler and history recording
  - Docker Compose env passthrough
- UI requested in this session:
  - title: `Nusantara AI - Voice Agent`
  - eyebrow: `Build your voice agent`
  - model/copy: `Grok Voice Think Fast 1.0`
  - instruction: `Pick a template or describe your own, then start a conversation.`
  - `Choose a template`
  - templates: Medical Office, Restaurant Host, Help Desk, Real Estate Agent, Book Appointments, Hotel Concierge, Create Custom
  - submit button: `Start`

## xAI realtime backend pattern
- Install backend WebSocket dependency if not already present:
  - `npm install ws @types/ws --save`
- Read secret from env only:
  - `XAI_API_KEY` preferred
  - `GROK_API_KEY` fallback/alias
- Add both vars to `config.ts`, `docker-compose.yml`, and env examples/placeholders.
- WebSocket endpoint observed in user-provided snippet:
  - `wss://api.x.ai/v1/realtime`
  - header: `Authorization: Bearer <env key>`
  - initial events:
    - `session.update` with `session: { voice: 'Eve', instructions: '...' }`
    - `conversation.item.create` with user `input_text`
    - `response.create`
  - useful transcript delta event: `response.output_audio_transcript.delta`
- Also capture `response.text.delta` defensively.
- Finish on `response.done` or `response.completed`.
- Use a bounded timeout so a stuck realtime connection does not hang the HTTP request.

## Verification
- Build first:
  - `npm run build:server && npm run build:web`
- Deploy:
  - `bash scripts/deploy.sh`
- Verify:
  - health local and public
  - `docker compose ps`
  - masked env check inside the container (`XAI_API_KEY=set`, never print value)
  - public model catalog contains the voice model and `enabled=true`
  - built JS bundle contains the requested labels/templates
  - source secret scan confirms pasted key is only in env files, not source
- A direct WebSocket probe returning HTTP `429` means the endpoint/auth path is reachable but rate-limited. Report it as rate limiting, not as a failed deploy.

## Pitfalls
- Do not hardcode or echo the xAI key in code, terminal output, or final response. If the user pasted it in chat, recommend rotation.
- Some patch/lint tools may run TS without the project tsconfig and show unrelated default-import/auth typing errors. Trust the project build script (`npm run build:server`) as the gate for this repo.
- If `ws` default import fails under a different TS config, use the import shape compatible with that project (`import WebSocket, { type RawData } from 'ws'` worked here under the official build).
