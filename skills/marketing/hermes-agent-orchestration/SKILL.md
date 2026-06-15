---
name: hermes-agent-orchestration
description: Use when coordinating Nusantara-AI content agents through Hermes Agent, including handoff contracts, queue routing, inter-agent communication, and safe execution boundaries.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, orchestration, multi-agent, handoff, nusantara-news, seedance]
    related_skills: [scheduler-agent, quality-check-agent, nusantara-news-pipeline-automation]
---

# Koneksi Hermes-Agent untuk Orkestrasi Antar Agen

## Overview

Skill ini mendefinisikan cara Hermes-Agent mengorkestrasi agent-agent Nusantara-AI agar bekerja sebagai pipeline terhubung, bukan instruksi terpisah. Hermes bertindak sebagai orchestrator yang mengatur urutan kerja, kontrak input/output, quality gate, scheduling, dan publikasi.

Agent utama:

1. Content Ideation Agent
2. Filter Agent
3. Script Writing Agent
4. Filter Agent
5. Visual & Audio Creation Agent
6. Filter Agent
7. Quality Check Agent
8. Scheduler Agent
9. Publishing/Distribution Agent

## When to Use

Gunakan skill ini saat user meminta:

- koneksi Hermes-Agent untuk komunikasi antar agen
- orkestrasi multi-agent Nusantara-AI
- membuat agent workflow otomatis dari ide sampai upload
- mengatur handoff antar agent
- menjalankan pipeline konten dengan beberapa agent
- memastikan output agent pertama menjadi input agent berikutnya

## Orchestration Principle

Hermes-Agent menjadi pusat koordinasi:

```text
Content Ideation Agent
  -> Filter Agent
  -> Script Writing Agent
  -> Filter Agent
  -> Visual & Audio Creation Agent
  -> Render Media
  -> Filter Agent
  -> Quality Check Agent
  -> Scheduler Agent
  -> Publishing/Distribution Agent
```

Setiap agent wajib menghasilkan output terstruktur agar agent berikutnya bisa memproses tanpa menebak.

## Agent Handoff Contract

### 1. Content Ideation Agent Output

```yaml
idea_packet:
  content_id: "..."
  topic: "..."
  trend_reason: "..."
  target_audience: "Indonesia/all-ages"
  angle: "..."
  source_context: "..."
  freshness: "..."
  sentiment: positive | neutral
  source_trust: trusted | internal_verified
  risk_notes: []
  suggested_hashtags: []
```

### 1B. Filter Agent Output

```yaml
filter_result:
  content_id: "..."
  decision: PASS | BLOCK | REVIEW
  blocked: true | false
  categories: []
  matched_count: 0
  severity: low | medium | high | critical
  safe_for_all_ages: true | false
```

Only `decision: PASS` may continue to the next agent.

### 2. Script Writing Agent Output

```yaml
script_packet:
  content_id: "..."
  judul: "..."
  hook: "..."
  script_narasi: "..."
  cta_akhir: "..."
  visual_direction: "..."
  durasi_estimasi: 30
  hashtags: []
  language_style: "baku-indonesia"
```

Catatan: `script_narasi` boleh digunakan untuk caption/metadata/struktur visual, tetapi tidak berarti OpenAI TTS aktif.

### 3. Visual & Audio Creation Agent Output

```yaml
visual_audio_packet:
  content_id: "..."
  provider: "seedance"
  use_reference_image: false
  generate_audio: true
  tts_provider: "disabled"
  video_prompt: "..."
  negative_prompt: "..."
  settings:
    aspect_ratio: "9:16"
    resolution: "1080x1920"
    duration: 30
    watermark: false
    no_running_text: true
  output:
    video_path: "..."
    manifest_path: "..."
```

### 4. Quality Check Agent Output

```yaml
quality_check:
  content_id: "..."
  total_score: 0
  decision: PUBLISH | RETRY | SKIP
  scores:
    duration_format: 0
    audio_quality: 0
    trend_fit: 0
    visual_brand_compliance: 0
  critical_issues: []
  recommended_fixes: []
```

### 5. Scheduler Agent Output

```yaml
scheduler_decision:
  content_id: "..."
  decision: SCHEDULE | PUBLISH_NOW | SKIP_SLOT | RETRY_LATER | HOLD
  scheduled_at: "ISO8601"
  targets:
    youtube_shorts: pending | uploaded | skipped | failed
    telegram: pending | sent | skipped | failed
    news_site: pending | published | skipped | failed
```

## Execution Rules

- Jangan lanjut ke agent berikutnya jika output agent sebelumnya tidak valid.
- Wajib jalankan Filter Agent sebelum Script Writing, sebelum Visual/Audio, dan sebelum publish. Jika `filter_result.decision` bukan `PASS`, item harus ditahan atau diblokir.
- Jangan publish jika Quality Check Agent memberi skor <90.
- Jangan publish jika `decision != PUBLISH`.
- Jangan menjalankan dua YouTube queue bersamaan.
- Jangan menampilkan credential/API key/token.
- Jangan menggunakan OpenAI TTS kecuali user eksplisit mengaktifkan ulang.
- Video default harus `NEWS_VIDEO_USE_REFERENCE_IMAGE=0`.
- Audio default harus generated-video audio/SEEDANCE ambience only.
- Semua content publik memakai Bahasa Indonesia baku.
- Normalisasi naskah wajib terjadi di handoff Script Writing Agent -> Visual & Audio Creation Agent: gunakan paket script yang sudah dibersihkan dari slang/singkatan dan mengikuti KBBI sebelum membuat prompt SEEDANCE, metadata publik, atau tahap apa pun yang dapat menghasilkan audio.
- Routine mode: Content Ideation Agent dapat berjalan setiap beberapa jam dan menulis `data/content-ideas/*`; Script Writing Agent mengikuti dengan `context_from` ideation job dan menulis `data/content-scripts/*`. Kedua tahap ini tidak boleh upload, kirim Telegram, atau memulai queue publikasi.

## Hermes Tooling Pattern

Untuk subtask cepat dan paralel, Hermes bisa memakai `delegate_task`:

```text
- Agent ideation: cari ide dan trend packet
- Agent script: ubah idea_packet jadi script_packet
- Agent visual: susun prompt SEEDANCE/video packet
- Agent QC: evaluasi manifest/video final
```

Untuk job 24 jam, gunakan queue/scheduler, bukan delegate_task panjang.

Untuk komunikasi lintas platform:

- Gateway Telegram/Discord/Slack bisa menerima trigger user.
- Hermes orchestrator membaca trigger.
- Pipeline menulis manifest/report.
- Scheduler mengirim hasil ke YouTube/Telegram/news site.

## Recommended Orchestration State

Simpan status per content item:

```yaml
orchestration_state:
  content_id: "..."
  stage: ideation | scripting | visual_audio | quality_check | scheduling | publishing | done | failed | skipped
  last_agent: "..."
  next_agent: "..."
  artifacts:
    idea_packet: "..."
    script_packet: "..."
    visual_audio_manifest: "..."
    quality_report: "..."
    scheduler_report: "..."
  error:
    code: "..."
    message: "..."
```

## Session References

- `references/session-2026-05-07-ideation-script-kbbi-handoff.md` — routine Content Ideation -> Script Writing cron handoff, storage paths, and KBBI/audio preflight checks.
- `references/session-2026-05-07-content-filter-and-script-style.md` — Filter Agent gate, forbidden-category config, cron updates, local validator, and `ringan-menarik-baku` script style.
- `references/session-2026-05-07-visual-audio-qc-agent-chain.md` — Visual & Audio Creation Agent plus Quality Check Agent configs, runners, cron jobs, dry-run/render/QC commands, and provider-billing blocker handling.
- `references/session-2026-05-07-full-agent-chain-buildout.md` — end-to-end class-level agent chain buildout from ideation to scheduler, stable repo artifacts, cron job IDs, cross-agent rules, and verification commands.
- `references/session-2026-05-07-automation-flow-v2-and-byte-docs.md` — latest Automation Flow V2, Byte1-Byte14 mapping, repo artifacts, max-30s gates, validation results, and BytePlus/ARK billing blocker handling.

## Common Pitfalls

1. Membiarkan agent output bebas tanpa format YAML/JSON sehingga agent berikutnya harus menebak.
2. Melompat dari script langsung upload tanpa Visual/QC gate.
3. Menjalankan queue baru tanpa cek queue lama.
4. Menganggap script narasi berarti TTS harus dibuat. Saat ini OpenAI TTS dimatikan.
5. Memakai image Instagram 4:5 sebagai reference video padahal mode default no-reference.
6. Menurunkan skor publish karena slot kosong. Slot harus skip.

## Verification Checklist

- [ ] Semua agent punya kontrak output terstruktur.
- [ ] Handoff content_id konsisten antar stage.
- [ ] SEEDANCE dipakai untuk video/audio generation.
- [ ] OpenAI TTS tetap disabled.
- [ ] Quality gate minimal 90 aktif sebelum scheduler.
- [ ] Scheduler tidak menjalankan double queue.
- [ ] Semua report/manifest ditulis dan bisa diaudit.
