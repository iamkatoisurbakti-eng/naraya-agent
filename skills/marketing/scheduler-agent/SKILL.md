---
name: scheduler-agent
description: Use when scheduling Nusantara-AI content publication with YouTube upload scheduling, hourly queue automation, public article autoposting, Telegram delivery, and safe publish windows.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [scheduler, youtube, autopost, queue, publishing, nusantara-news]
    related_skills: [nusantara-news-pipeline-automation, quality-check-agent]
---

# Agen Penjadwal

## Overview

Agen Penjadwal mengatur kapan konten Nusantara-AI dipublikasikan ke YouTube Shorts dan kanal distribusi lain. Agent ini memakai integrasi upload/scheduler YouTube yang sudah ada di pipeline, menjaga antrean 24 jam, dan memastikan hanya konten yang lolos skor serta quality gate yang dipublikasikan.

Agent ini bukan pembuat konten. Ia menerima output dari Content Ideation Agent, Script Writing Agent, Visual & Audio Creation Agent, dan Quality Check Agent, lalu menentukan slot publikasi, menjalankan upload/scheduling YouTube melalui YouTube Scheduler API/OAuth, dan mencatat hasilnya. Upload hanya boleh berjalan jika QC `decision=PUBLISH`, skor minimal 90, video final valid, dan credential OAuth tersedia.

## When to Use

Gunakan skill ini saat user meminta:

- menjadwalkan upload YouTube Shorts
- menjalankan antrean 1 jam 1 video
- menjalankan publikasi otomatis 24 jam
- membuat scheduler agent untuk pipeline Nusantara-AI
- mengatur autopost artikel, Telegram, Facebook, atau Instagram-ready assets
- memastikan konten yang lolos QC saja yang diunggah
- mengecek queue berjalan atau tidak
- mencegah double upload karena ada dua queue aktif

Jangan gunakan untuk:

- membuat ide konten dari nol
- menulis script Shorts
- generate video/audio
- mengevaluasi kualitas konten secara mendalam; gunakan Quality Check Agent terlebih dahulu

## Role Prompt

Kamu adalah Agen Penjadwal Nusantara-AI News.

Tugas kamu adalah mengatur publikasi konten berdasarkan antrean, skor, quality check, dan waktu upload yang optimal. Kamu harus memastikan tidak ada double upload, tidak ada konten skor rendah yang dipaksa publish, dan semua credential tetap disimpan di environment variables.

Keputusan utama:

- SCHEDULE: konten masuk slot publikasi.
- PUBLISH_NOW: konten langsung dipublikasikan jika user meminta dan semua gate lolos.
- SKIP_SLOT: slot dilewati karena konten tidak cukup baik, duplikat, provider gagal, atau credential kurang.
- RETRY_LATER: coba lagi di slot berikutnya karena error provider/rate-limit.
- HOLD: tahan publikasi karena QC/gate belum lengkap.

## Inputs

```yaml
content_id: string
run_dir: string
manifest_path: string
video_path: string
image_path: string
article_path: string
article_url: string
quality_check:
  total_score: number
  decision: PUBLISH | RETRY | SKIP
news_score: number
publish_targets:
  youtube_shorts: boolean
  telegram: boolean
  news_site: boolean
  facebook: boolean
  instagram_ready_asset: boolean
schedule:
  mode: hourly_queue | exact_time | publish_now | daily_batch
  start_time: ISO8601 | null
  interval_seconds: number
  slots: number
  timezone: Asia/Jakarta
metadata:
  title: string
  description: string
  tags: string[]
  made_for_kids: false
  privacy_status: public | private | unlisted
```

## Required Gates Before Scheduling

Konten hanya boleh dijadwalkan jika semua gate ini lolos:

1. `news_score >= 90`.
2. `quality_check.total_score >= 90`.
3. `quality_check.decision == PUBLISH`.
4. Video final ada dan bisa dibaca.
5. Video 9:16, minimal 1080x1920.
6. Video punya audio jika audio diwajibkan.
7. Tidak ada OpenAI TTS default.
8. Tidak ada running text/ticker/subtitle bergerak.
9. Tidak ada watermark.
10. Tidak duplikat berdasarkan history dan public article index.
11. YouTube OAuth siap jika target YouTube aktif.
12. Telegram token dan target channel siap jika target Telegram aktif.
13. Public article berhasil dibuat jika target news site aktif.

Jika gate gagal, jangan publish. Tandai slot sebagai `skipped_quality_gate`, `skipped_duplicate`, `skipped_missing_credentials`, atau reason spesifik lain.

## YouTube Scheduler Rules

Gunakan integrasi YouTube OAuth, bukan API key biasa.

Credential wajib ada di env:

- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

Jangan pernah mencetak nilainya.

Default publikasi Nusantara-AI:

```env
YOUTUBE_PRIVACY_STATUS=public
YOUTUBE_MADE_FOR_KIDS=0
YOUTUBE_TARGET_COUNTRY=ID
YOUTUBE_DEFAULT_LANGUAGE=id
YOUTUBE_LOCATION_DESCRIPTION=Indonesia
YOUTUBE_CATEGORY_ID=25
YOUTUBE_GROWTH_MODE=1
NEWS_YOUTUBE_GROWTH_MODE=1
```

Untuk antrean 24 jam:

```env
YOUTUBE_QUEUE_SLOTS=24
YOUTUBE_QUEUE_INTERVAL_SECONDS=3600
YOUTUBE_QUEUE_MONITOR_HOURS=24
YOUTUBE_UPLOAD_COUNT=1
NEWS_MIN_SCORE=90
NEWS_MIN_SINGLE_SCORE=90
NEWS_STRICT_NO_DUPLICATE=1
NEWS_HISTORY_MAX_ITEMS=240
NEWS_ARTICLE_AUTOPOST=1
```

## YouTube Scheduler API Mode

Scheduler lokal Nusantara-AI memakai file konfigurasi:

- `/root/nusantara-ai-saas/config/scheduler-agent.json`

Runner:

- `/root/nusantara-ai-saas/scripts/scheduler-agent.mjs`

Aturan:
- Baca hasil QC dari `/root/nusantara-ai-saas/data/quality-check/latest.json`.
- Jangan upload jika `quality_check.decision != PUBLISH` atau `total_score < 90`.
- Jangan upload jika video file tidak ada, bukan 9:16, kurang dari 1080x1920, atau audio wajib tidak ada.
- Jangan upload jika YouTube OAuth env belum lengkap.
- Gunakan OAuth env `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`; jangan API key biasa.
- Gunakan `YOUTUBE_PRIVACY_STATUS`, `YOUTUBE_MADE_FOR_KIDS`, `YOUTUBE_DEFAULT_LANGUAGE`, `YOUTUBE_TARGET_COUNTRY`, dan `YOUTUBE_CATEGORY_ID` sebagai defaults.
- Default scheduling policy: `hourly_queue`, 1 slot per jam, maksimal 24 slot, timezone `Asia/Jakarta`.
- Jika ada queue upload aktif lain, beri keputusan `HOLD`/`SKIP_SLOT`, jangan memulai double upload.
- Untuk dry-run, hanya tulis `scheduler_decision` tanpa memanggil upload.
- Jika user meminta **"run sekali sekarang"** atau test ad-hoc, jangan mengandalkan `cronjob run` saja; itu bisa hanya menggeser `next_run_at` tanpa membuktikan eksekusi. Jalankan runner/pipeline yang sesungguhnya bila tersedia, lalu verifikasi artefak/log/delivery sebelum melaporkan sukses.

## Publication Flow

1. Terima hasil dari Quality Check Agent.
2. Untuk automation berita rutin baru, biasakan satu cron job komposit yang mencakup fetch → scoring → render → deliver, kecuali user meminta pemisahan stage secara eksplisit.
3. Setelah create, verifikasi langsung dengan `cronjob list` agar job_id, schedule, dan enabled state benar.
2. Verifikasi score dan publish readiness.
3. Cek tidak ada queue aktif lain.
4. Pilih slot publikasi:
   - publish_now untuk permintaan langsung
   - hourly_queue untuk 1 jam 1 video
   - exact_time untuk jadwal spesifik
   - daily_batch untuk batch harian
5. Jalankan upload YouTube jika target aktif.
6. Simpan public article jika target news site aktif.
7. Kirim Telegram setelah image dan video final ada.
8. Posting Facebook Page jika `META_PAGE_ACCESS_TOKEN` tersedia.
9. Tulis state/report queue.
10. Jika gagal karena provider/billing/rate-limit, jangan double upload; retry slot berikutnya.

## Recommended Commands

Jalankan dari repo:

```bash
cd /root/nusantara-ai-saas
```

Dry-run pipeline:

```bash
NEWS_VIDEO_USE_REFERENCE_IMAGE=0 NEWS_NATURAL_NARRATION=0 NEWS_TTS_PROVIDER=disabled npm run gen:news-pipeline -- --count 1 --dry-run --skip-youtube --skip-telegram
```

One-off YouTube scheduled upload:

```bash
npm run gen:news-youtube-upload -- --count 1
```

Start hourly queue with Telegram delivery:

```bash
YOUTUBE_QUEUE_SLOTS=24 YOUTUBE_QUEUE_INTERVAL_SECONDS=3600 YOUTUBE_QUEUE_MONITOR_HOURS=24 YOUTUBE_UPLOAD_COUNT=1 NEWS_ARTICLE_AUTOPOST=1 scripts/run-youtube-hourly-queue.sh --send-telegram
```

Queue state:

```bash
cat /root/nusantara-ai-saas/data/logs/youtube-hourly-queue-state.json
```

Queue log:

```bash
tail -100 /root/nusantara-ai-saas/data/logs/youtube-hourly-queue.log
```

Note: di Hermes tools, gunakan `read_file`/`process` daripada `cat`/`tail` bila tersedia.

## Output Format

```yaml
scheduler_decision:
  content_id: "..."
  decision: SCHEDULE | PUBLISH_NOW | SKIP_SLOT | RETRY_LATER | HOLD
  reason: "..."
  slot:
    mode: hourly_queue | exact_time | publish_now | daily_batch
    scheduled_at: "ISO8601"
    timezone: "Asia/Jakarta"
  gates:
    news_score_ok: true
    quality_score_ok: true
    video_ready: true
    youtube_oauth_ready: true
    telegram_ready: true
    article_ready: true
    duplicate_check_ok: true
  targets:
    youtube_shorts: pending | uploaded | skipped | failed
    telegram: pending | sent | skipped | failed
    news_site: pending | published | skipped | failed
    facebook: pending | posted | skipped | failed
  files:
    video_path: "..."
    image_path: "..."
    article_url: "..."
  notes:
    - "..."
```

## Duplicate Queue Safety

Sebelum memulai queue baru:

1. Cek proses aktif Hermes/background.
2. Jika queue lama masih aktif dan konfigurasi sama, jangan start ulang.
3. Jika harus ganti konfigurasi, hentikan queue lama secara sengaja lalu mulai queue baru.
4. Exit code `-15` dari queue lama yang sengaja dihentikan adalah SIGTERM terkontrol, bukan crash.
6. Jangan menjalankan dua queue upload otomatis bersamaan.
7. Jika user minta `stop automation`, `pause`, atau `hapus semua paused`, gunakan cronjob `list` dulu untuk mengidentifikasi target, lalu `pause` untuk stop sementara atau `remove` untuk hapus permanen, dan selalu verifikasi dengan `list` ulang sampai count turun sesuai harapan.
8. Jika user minta "run sekarang", jangan mengandalkan `cronjob run` saja untuk menghasilkan output instan; verifikasi apakah itu hanya menjadwalkan tick berikutnya dan, bila perlu, panggil runner/pipeline yang sebenarnya secara langsung lalu cek artefak/delivery.
9. Jika user meminta merapikan jadwal agar tidak tabrakan, treat it as queue hygiene: list jobs first, identify the exact job_id to prune, remove only the overlapping job unless user asks for full reschedule, then list again to confirm the remaining schedule spacing.

See `references/session-2026-05-09-ksr888-job-queue-organization.md` for the KSR888-specific prune/verify pattern from this session.


See `references/session-2026-05-08-cron-run-immediate-and-telegram-target.md` for the observed `cronjob run` behavior and Telegram target mapping pitfall.
See `references/session-2026-05-08-cronjob-stop-pause-remove.md` for the observed Hermes cronjob stop/pause/remove workflow.

## Error Handling

- `AccountOverdueError` / HTTP 403 dari ARK/BytePlus/SEEDANCE: tandai `RETRY_LATER` atau `SKIP_SLOT`, bukan bug YouTube.
- OpenAI `gpt-image-2` HTTP 403 organization verification: tandai image provider blocker; queue boleh tetap hidup, tetapi jangan klaim media/publish berhasil sampai organisasi OpenAI verified dan real image generation sukses.
- Jika queue live berjalan tetapi slot pertama gagal, laporkan dua status terpisah: scheduler/process running vs production output blocked. Baca `data/logs/youtube-hourly-queue-state.json` sebelum menyatakan hasil.
- YouTube OAuth gagal: `HOLD` sampai refresh token diperbaiki.
- Telegram upload terlalu besar: kompres preview atau skip Telegram video; jangan gagalkan YouTube jika YouTube sudah sukses.
- Meta token missing: skip Facebook saja.
- QC skor <90: `SKIP_SLOT`.
- Tidak ada kandidat unik: `SKIP_SLOT` reason `no_unique_viral_news`.

## Reference Notes

- See `references/session-2026-05-07-youtube-scheduler-agent.md` for the local scheduler runner/config, cron job ID, gate order, dry-run command, observed SKIP_SLOT result, and duplicate-queue/provider-billing pitfalls from the first Scheduler Agent setup.
- See `references/session-2026-05-08-hourly-news-debate-score-publish.md` for the composite hourly news cron pattern created in this session and the post-create `cronjob list` verification habit.

## Common Pitfalls

1. Menggunakan API key biasa untuk upload YouTube. Upload butuh OAuth refresh token.
2. Memulai queue baru tanpa mematikan queue lama sehingga double upload.
3. Mengunggah konten yang belum lulus QC.
4. Menganggap slot kosong sebagai alasan menurunkan standar skor.
5. Mencetak secret dari `.env`.
6. Memakai OpenAI TTS padahal user sudah mematikan OpenAI TTS default.
7. Mengirim Telegram sebelum image dan video final ada.
8. Menyimpulkan `cronjob run` berarti eksekusi langsung selesai. Di Hermes, trigger manual bisa hanya menjadwalkan tick berikutnya; selalu cek `last_run_at`, `last_status`, dan log delivery sebelum mengklaim Telegram terkirim.

## Verification Checklist

- [ ] Tidak ada queue duplikat.
- [ ] YouTube OAuth set tanpa mencetak secret.
- [ ] Konten lolos news score >=90.
- [ ] Konten lolos Quality Check Agent score >=90.
- [ ] Video final ada, 9:16, minimal 1080x1920, audio ada.
- [ ] Article output ada jika autopost aktif.
- [ ] Telegram target siap jika send Telegram aktif.
- [ ] State/report queue ditulis.
- [ ] Keputusan SCHEDULE/PUBLISH_NOW/SKIP_SLOT/RETRY_LATER/HOLD tercatat jelas.
- [ ] Setelah prune/recreate job, `cronjob list` sudah dicek ulang dan schedule tidak saling tabrakan.
