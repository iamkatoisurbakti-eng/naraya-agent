# OpenAI Audio notes for Nusantara-AI News automation

Source imported from `/root/OpenAI Audio` on 2026-05-07.

## Relevant automation decision

For deterministic news presenter narration, use the OpenAI Audio API `audio/speech` endpoint rather than free-form `gpt-audio` chat output. This keeps the narration script controlled by the pipeline while still allowing natural voice instructions.

Current implementation:
- Script: `/root/nusantara-ai-saas/scripts/news-video-natural-narration.ts`
- Endpoint: `POST /v1/audio/speech`
- Default model: `gpt-4o-mini-tts`
- Default voice: `verse`
- Default output format: `mp3`
- Required env: `OPENAI_API_KEY`
- Optional env: `OPENAI_BASE_URL`, `NEWS_TTS_MODEL`, `NEWS_TTS_VOICE`, `NEWS_TTS_FORMAT`

## Key points from OpenAI Audio file

- Text-to-speech should use the Audio API `audio/speech` endpoint.
- Models compatible with speech include `gpt-4o-mini-tts`, `tts-1`, and `tts-1-hd`.
- `gpt-4o-mini-tts` supports tone/style instructions, useful for presenter-style Indonesian narration.
- Speech-to-text uses `audio/transcriptions` with models such as `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `whisper-1`, and `gpt-4o-transcribe-diarize`.
- Realtime API is for low-latency voice agents; not needed for scheduled news video autoposting.
- Chat Completions with `gpt-audio` can produce audio directly, but it is less deterministic because the model can generate its own spoken response. For news automation, keep text script generation separate from TTS.

## Pipeline usage

When the main news pipeline creates a titled MP4, run:

```bash
npm run gen:news-video:natural-narration -- \
  --video-manifest <video-title-manifest.json> \
  --news-manifest <manifest.json>
```

For dry-run:

```bash
npm run gen:news-video:natural-narration -- \
  --dry-run \
  --video-manifest <video-title-manifest.json> \
  --news-manifest <manifest.json>
```

The output manifest points `titleVideoPath` to the narrated MP4 when TTS succeeds, so Telegram/YouTube can consume the same final manifest.
