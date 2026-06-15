# GeminiGenAI Veo3 API notes

Context: integrating https://github.com/GeminiGenAI/Veo3-AI-Video-API into the Nusantara AI SaaS video generator.

Observed integration shape
- Base URL: `https://api.geminigen.ai`
- Create video: `POST /api/video-gen/veo`
- Poll job/history: `GET /api/history/{uuid}`
- Auth headers used in the app integration: `Authorization: Bearer <API_KEY>` and `apikey: <API_KEY>`

Model ids surfaced in the app
- `veo-3-fast`
- `veo-3.1-lite`
- `veo-3`
- `veo-2`

Payload shape used by the app
- `prompt`
- `model`
- `aspect_ratio` (`16:9` or `9:16`)
- `duration`
- `resolution` (`720p` or `1080p`)
- `enhance_prompt`
- `num_videos`
- Optional media fields appended as form-data blobs:
  - `ref_images`
  - `reference_video`
  - `reference_audio`

Runtime behavior
- The create response may include a finished video URL immediately or only a task id/uuid.
- Poll history until the job reports success or returns a playable URL.
- Mirror successful remote video URLs into local generated media storage before saving history so previews do not depend on expiring provider links.

Practical pitfalls
- Keep provider secrets in env vars only.
- Update backend config, Docker Compose env passthrough, and frontend build-time env handling together when adding a new provider key.
- Video model option lists should be model-specific; do not leave VEO durations/ranges tied to a generic `veo` catch-all.
- The public UI should show customer-friendly model labels, but the backend should normalize aliases like `veo-3.1` / `veo3` to the canonical model id before calling the provider.