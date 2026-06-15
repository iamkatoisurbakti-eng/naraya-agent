# Seedance native audio default

Use this when Seedance video generation returns silent videos or the user asks for generated video with audio.

## Pattern
- Treat audio as an explicit video option, not an afterthought in the prompt only.
- Frontend Video Studio should default `nativeAudio`/audio bawaan to enabled for Seedance-capable video generation.
- When the selected video model changes, reset/keep audio enabled unless the user explicitly disables it for the current generation.
- Backend should be defensive: interpret missing `nativeAudio` as enabled (`body.nativeAudio !== false`) so older frontend bundles and API callers still request audio.
- Provider payload for ModelArk/Seedance should include the provider audio flag, e.g. `generate_audio: true`, plus a prompt instruction such as synchronized native audio, ambience, sound effects, and motion-matched sound.
- Keep the UI label user-friendly: “Audio bawaan aktif…” instead of exposing provider field names.

## Verification without spending video credits
- Run `npm run build:server && npm run build:web` and relevant API tests.
- Deploy via the project script.
- Verify production health.
- Grep the compiled server output for `generate_audio`, `body.nativeAudio !== false`, and the audio instruction text.
- Grep/fetch the production JS bundle for the user-facing audio label.
- Do not run a real Seedance generate smoke unless explicitly approved because it consumes provider/credit budget.
