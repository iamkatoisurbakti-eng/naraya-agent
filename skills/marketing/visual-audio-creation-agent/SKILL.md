---
name: visual-audio-creation-agent
description: Use when converting Nusantara-AI script_packet outputs into YouTube Shorts visual/audio production packets and SEEDANCE text-to-video jobs with relevant clips, images, and generated ambience audio.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [visual-audio, seedance, youtube-shorts, nusantara-news, no-openai-tts]
    related_skills: [script-writing-agent, filter-agent, quality-check-agent, hermes-agent-orchestration, nusantara-news-pipeline-automation]
---

# Visual & Audio Creation Agent

## Overview

Visual & Audio Creation Agent menerima `script_packet` yang sudah lolos Filter Agent dan mengubahnya menjadi paket produksi video YouTube Shorts. Agent ini menghasilkan cuplikan/adegan visual, gambar pendukung, dan suara ambience/action yang relevan melalui SEEDANCE/text-to-video. Agent ini tidak upload, tidak menjadwalkan, dan tidak mengirim Telegram.

## Input

```yaml
script_packet:
  content_id: "..."
  judul: "..."
  hook: "..."
  script_narasi: "..."
  cta_akhir: "..."
  visual_direction: "..."
  durasi_estimasi: 35
  hashtags: []
  language_style: "ringan-menarik-baku"
  no_openai_tts: true
```

Input wajib memiliki `filter_result.decision=PASS`.

## Output Contract

```yaml
visual_audio_packet:
  content_id: "..."
  provider: "seedance"
  stage: visual_audio
  status: READY | RENDERED | BLOCKED_BY_FILTER | FAILED
  use_reference_image: false
  generate_audio: true
  tts_provider: "disabled"
  video_prompt: "..."
  negative_prompt: "..."
  image_prompt: "..."
  scenes:
    - scene: 1
      duration_seconds: 15
      visual: "..."
      audio: "copyright-safe original ambience/action sound only"
  settings:
    aspect_ratio: "9:16"
    resolution: "1080x1920"
    duration_seconds: 30
    scene_count: 2
    scene_duration_seconds: 15
    watermark: false
    no_running_text: true
    no_reference_image: true
    copyright_safe: true
  output:
    video_path: "..."
    manifest_path: "..."
```

## Hard Rules

- Default video: YouTube Shorts 9:16, `1080x1920`, 30 fps, HD, durasi maksimal 30 detik.
- Gunakan SEEDANCE/text-to-video prompt-only: `NEWS_VIDEO_USE_REFERENCE_IMAGE=0`.
- Jangan memakai Instagram 4:5 image sebagai reference video kecuali user eksplisit meminta.
- Audio: generated-video audio/SEEDANCE ambience/action only.
- Jangan menggunakan OpenAI TTS, `/audio/speech`, voice-over, dialog, atau musik populer.
- Jangan menjalankan `scripts/news-video-natural-narration.ts`.
- Visual harus cinematic realistic action/event-scene yang relevan dengan berita.
- Jangan reporter, anchor, newsroom, poster teks, running text, subtitle bergerak, watermark, platform UI, logo/IP terkenal, selebritas/impersonasi, stock/TV/social clip.
- Semua text prompt harus Bahasa Indonesia baku/KBBI-style setelah normalisasi.
- Wajib jalankan Filter Agent sebelum render; jika bukan PASS, status `BLOCKED_BY_FILTER`.
- Jangan upload YouTube/Telegram/Facebook; output hanya file/manifest untuk Quality Check Agent.

## Prompt Formula

Gabungkan:
1. Judul berita
2. Hook ringkas
3. Naskah/visual_direction yang sudah dibersihkan dari frasa negatif seperti `tanpa reporter`, `tanpa teks berjalan`, `tanpa watermark`
4. 2 adegan masing-masing maksimal 15 detik; total video wajib maksimal 30 detik
5. Instruksi cinematic realistis
6. Instruksi audio ambience/action original
7. Negative prompt terpisah untuk no text/no watermark/no reporter/no anchor/no newsroom

Filter Agent harus memeriksa prompt positif/publik, bukan `negative_prompt`, karena negative prompt memang berisi kata-kata yang dilarang sebagai instruksi pengecualian.

## Storage Convention

Simpan hasil rutin ke:
- `/root/nusantara-ai-saas/data/visual-audio/visual-audio-YYYY-MM-DD.jsonl`
- `/root/nusantara-ai-saas/data/visual-audio/latest.json`
- video/manifest render di `/root/nusantara-ai-saas/data/visual-audio/renders/`

## Reference Notes

- See `references/session-2026-05-07-visual-audio-agent-setup.md` for the first Nusantara-AI Visual & Audio Agent setup, cron job ID, runner/config paths, validation commands, false-positive filter lesson for negative prompts, and ARK/BytePlus `AccountOverdueError` handling.
- See `nusantara-news-pipeline-automation/references/openai-gpt-image-2-provider.md` for the image-only GPT Images 2.0 switch. Important: GPT Images changes Instagram/news image generation only; Shorts video rendering still uses SEEDANCE/ARK unless the video provider is explicitly changed, so ARK video blockers remain possible.
- See `nusantara-news-pipeline-automation/references/byteplus-ark-byte1-byte14-automation.md` for BytePlus/ARK Byte1-Byte14 mapping. Use Byte4 as Seedance video API reference and Byte13 as prompt-only text-to-video example; keep current Nusantara-AI overrides: no reference image by default, no OpenAI TTS, generated ambience audio, no watermark, 2×15s scenes, max 30 seconds.

## Session References

- `hermes-agent-orchestration/references/session-2026-05-07-visual-audio-qc-agent-chain.md` — concrete Nusantara-AI repo runner/config/cron setup, dry-run/render commands, and provider `AccountOverdueError` handling.

## Verification Checklist

- [ ] Input script_packet lolos Filter Agent.
- [ ] `NEWS_VIDEO_USE_REFERENCE_IMAGE=0`.
- [ ] `NEWS_TTS_PROVIDER=disabled` dan `NEWS_NATURAL_NARRATION=0`.
- [ ] Prompt positif tidak mengandung running text/watermark/reporter/anchor/newsroom; istilah tersebut hanya boleh muncul di `negative_prompt` terpisah.
- [ ] Output aspect ratio 9:16 dan target 1080x1920.
- [ ] Audio berasal dari generated-video ambience/action, bukan OpenAI TTS.
- [ ] Manifest siap diteruskan ke Quality Check Agent.
