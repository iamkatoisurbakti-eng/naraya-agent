# Advanced video studio controls

Use this reference when adding richer video generation controls to a React + Express studio UI.

## UI controls that should ship together
- Keyframes:
  - `startKeyframe`: accepts prose or a start image URL.
  - `endKeyframe`: accepts prose or an end image URL.
- Reference media fields:
  - `referenceImageUrl` / `firstFrameImageUrl`
  - `referenceVideoUrl`
  - `referenceAudioUrl`
- Video generation settings:
  - duration: selected-model-specific options, not one global list
  - quality: standard/high/ultra if supported
  - `enhancePrompt`: boolean toggle
  - `nativeAudio`: boolean toggle

## Prompt diversity / anti-repetition rule
- Treat template presets and fixed style menus as optional, not default required controls. If users report repeated/same-looking videos, remove Template/Style UI and stop sending `videoTemplate`, `templatePrompt`, and `style` from the frontend.
- Also remove those fields from the backend request type and provider prompt composition; hiding the UI while the server still appends style/template text will keep causing repeated content.
- Keep user-entered prompt, duration, ratio, quality, keyframes, reference media, enhance prompt, and native audio. These preserve useful control without forcing the same visual recipe every generation.

## Backend payload handling
Extend the generation body and pass the fields through the authenticated `/api/generate` route. Keep provider-specific prompt assembly on the server, not only in the UI.

Recommended server prompt composition for video:
1. Enhance prompt clause when `enhancePrompt` is true.
2. User prompt.
3. Start keyframe prose.
4. End keyframe prose.
5. Reference video URL note.
6. Reference audio URL note.
7. Native audio clause.
8. Quality and validated duration/ratio.

Do not append fixed template/style clauses unless the current product intentionally wants prescriptive presets. For open-ended creative video generation, fixed templates/styles tend to homogenize outputs.

## URL validation pattern
- For explicit media reference fields, require HTTPS and reject invalid non-empty values with a 400.
- For keyframe fields that can be prose or URLs, use the value as an image URL only when it starts with HTTPS; otherwise leave it as prompt text.
- Do not allow raw local paths or non-HTTPS URLs to reach provider APIs.

## FAL/minimax mapping used in this repo
- `referenceImageUrl` can map to `image_url` as the first frame.
- `endKeyframe` maps to `end_image_url` only if it is an HTTPS URL.
- Reference video/audio and native audio are embedded in the prompt text unless the selected provider exposes dedicated parameters.

## Verification
- Run server + web builds before deploy.
- Deploy through `bash scripts/deploy.sh`.
- Verify health endpoint and healthy Docker container.
- Search the production bundle for expected retained labels such as `Keyframe Start`, `Reference Audio`, audio label copy, `Duration`, and `Quality`.
- If removing repetition-causing presets, verify the live bundle no longer contains `Template Video`, `Pakai template ke prompt`, template preset labels, `videoTemplate`, `templatePrompt`, or `Style` menu labels.
