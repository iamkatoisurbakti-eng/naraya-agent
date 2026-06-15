# Session note: agent workflow with Seedance video/audio and no OpenAI TTS

Context: user defined a multi-agent Nusantara Shorts workflow and corrected audio policy.

Key learning:
- Content Ideation Agent should generate trend-aware ideas for Shorts and can use SEEDANCE/API-backed trend/media signals when integrated; it feeds Script Writing Agent.
- Script Writing Agent turns a content idea into a short Shorts script: title, hook, narration text, CTA, visual direction, duration, hashtags.
- Visual & Audio Creation Agent turns the script into Seedance text-to-video production prompts and payloads.
- Current video mode is prompt-only: do not pass Instagram 4:5 image/reference media into Seedance unless explicitly re-enabled.
- Current audio mode is generated-video audio/ambience only: do not use OpenAI TTS, `/audio/speech`, or `scripts/news-video-natural-narration.ts` unless explicitly re-enabled by the user.

Visual & Audio Creation Agent requirements:
- SEEDANCE text-to-video, 9:16, >=1080x1920.
- `generate_audio=true`, `use_reference_image=false`, `watermark=false`.
- Cinematic realistic action / Indonesian news documentary style.
- Generated original ambience/action audio only; no voice-over, no presenter, no dialog, no popular music or melody imitation.
- No reporter, anchor, newsroom, studio, poster-text visuals, running text, subtitle, ticker, lower-third motion, social UI, brand logos, watermarks, celebrity likeness, copyrighted characters, TV/movie/social clips.
- Center-safe composition with lower overlay-safe area reserved for static Nusantara-AI News template.

Operational defaults captured:
- `NEWS_VIDEO_USE_REFERENCE_IMAGE=0`
- `NEWS_NATURAL_NARRATION=0`
- `NEWS_TTS_PROVIDER=disabled`
- `NEWS_GENERATED_VIDEO_AUDIO_ENABLED=1`
- `NEWS_GENERATED_VIDEO_AUDIO_VOLUME=1.00`
- `NEWS_NARRATION_VOLUME=0`
- `NEWS_BACKSOUND_ENABLED=0`
- `NEWS_VIDEO_CINEMATIC_REALISM=1`
- `NEWS_VIDEO_NO_RUNNING_TEXT=1`
- `NEWS_VIDEO_WATERMARK=0`

Pitfall fixed:
- Older skill text still implied natural presenter narration/OpenAI TTS as default. That is now wrong for this user's active workflow. Treat OpenAI TTS as opt-in only.
