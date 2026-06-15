# Video Studio dynamic duration and numeric ratio controls

Use this when a video studio model selector changes but the duration/ratio controls stay static or send provider-invalid options.

## Pattern
- Keep backend model catalog as the source of truth for video model options where possible. Add per-video-model metadata to `/api/models/catalog` such as:
  - `supportedDurations: number[]`
  - `aspectRatios: string[]` using numeric strings like `16:9`, `9:16`, `1:1`
- Keep `/api/models/studio` deterministic if existing exact API tests compare it to static catalog output. If needed, expose new option metadata only on `/api/models/catalog` and let the frontend already loaded catalog drive the UI.
- In the React studio, derive current options from the selected model:
  - read `selectedModel.supportedDurations` / `selectedModel.aspectRatios`
  - provide a frontend fallback map for static/older responses
  - on model change, reset `duration` and `aspectRatio` when the previous value is not supported by the new model
- Render ratio labels as numbers, not prose: `16:9`, `9:16`, `1:1`. Apply this consistently across Video Studio, Images Studio, AI Clipper output format selectors, and public landing badges; avoid mixed labels such as `Landscape`, `Portrait`, `Square`, `Vertical Short`, `Landscape Clip`, or `Square Social`.
- Backend generate/clipper defaults should also use numeric ratios (for example `16:9` or `9:16`) while remaining backward-compatible with legacy prose payloads.
- Backend generate route must validate/coerce duration against the selected model too; do not rely only on UI dropdowns.
- If duration affects credit cost, route the same coerced duration into both `/api/generate/quote` and the final `/api/generate` charge path. The frontend quote effect must include `duration` in the query string and dependency array so the displayed credits update when the user changes the dropdown.
- Keep old ratio values compatible server-side (`landscape`, `portrait`, `square`) while emitting numeric ratios from the UI.
- Avoid hidden prompt modifiers that make video outputs repetitive. Do not auto-append selected `style`, `videoTemplate`, or `templatePrompt` values to provider prompts unless explicitly requested; if users report similar/repeated video content, remove template/style UI controls and strip those fields from the generate payload/options text so the user prompt remains the primary creative input.
- For Seedance/native-audio requests, default `nativeAudio` to enabled in the UI and backend (`body.nativeAudio !== false`), pass `generate_audio: true` where supported, and add a brief provider prompt instruction for synchronized ambience/sound effects. Do not run paid video smoke tests just to verify this; verify code/bundle strings and health instead.

## Example model rules used in Nusantara AI SaaS
- `seedance-2` / `dreamina-seedance-2*`: durations `[3, 5, 10, 15]`, ratios `[16:9, 9:16, 1:1]`
- `seedance-1.5*`, `seedance-1.0-pro*`: durations `[5, 10, 15]`
- `seedance-1.0-lite-i2v*`: duration `[5]`, ratios `[16:9, 9:16]`
- `veo*`: duration `[8]`
- `pixverse*`: durations `[5, 8]`
- `kling*` / `runway*`: durations `[5, 10]`
- `wan*`: duration `[5]`, ratios `[16:9, 9:16]`

## Verification
- `npm run build:server && npm run build:web`
- Run API tests; if exact `/studio` tests fail because of new metadata, either update tests intentionally or keep metadata on `/catalog` only.
- After deploy, query `/api/models/catalog` and verify representative model options without printing secrets:
  - `seedance-2` shows `[3,5,10,15]`
  - lite i2v shows `[5]`
  - `veo-3-1` shows `[8]`
- If pricing depends on duration, register/login with a temporary smoke user, call `/api/generate/quote?capability=video&model=seedance-2&duration=3|5|10|15`, verify increasing credit costs, then delete the smoke user from live DB. This verifies pricing without spending provider credits.
- Verify production health and Docker container healthy.
