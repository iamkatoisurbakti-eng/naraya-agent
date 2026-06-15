---
name: filter-agent
description: Use when filtering Nusantara-AI content ideas, scripts, captions, prompts, metadata, or publication packets against forbidden keywords/categories before handoff or production.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [content-filter, safety, moderation, nusantara-news, all-ages]
    related_skills: [content-ideation-agent, script-writing-agent, hermes-agent-orchestration, quality-check-agent]
---

# Filter Agent

## Overview

Filter Agent adalah gate khusus untuk memblokir konten Nusantara-AI yang mengandung kata kunci/topik terlarang sebelum masuk ke Script Writing Agent, Visual & Audio Creation Agent, produksi suara/audio, video, upload, atau publikasi.

Kategori terlarang utama:
- pornografi/seks eksplisit
- pedofilia/eksploitasi anak
- kekerasan/gore/kriminal sadis
- agama/SARA/konflik keagamaan
- politik/kampanye/partai/pemilu/tokoh politik

## Position in Pipeline

Gunakan Filter Agent di semua titik berikut:

```text
Content Ideation Agent
  -> Filter Agent
  -> Script Writing Agent
  -> Filter Agent
  -> Visual & Audio Creation Agent
  -> Filter Agent
  -> Quality Check Agent
  -> Scheduler Agent
```

Jika Filter Agent memberi `BLOCK`, item tidak boleh diteruskan. Jika `REVIEW`, item ditahan/manual review. Hanya `PASS` yang boleh lanjut.

## Input

Filter Agent menerima teks gabungan dari:
- `idea_packet.topic`
- `idea_packet.angle`
- `idea_packet.trend_reason`
- `idea_packet.source_context`
- `script_packet.judul`
- `script_packet.hook`
- `script_packet.script_narasi`
- `script_packet.cta_akhir`
- `script_packet.visual_direction`
- caption, hashtag, metadata, dan video prompt positif

Catatan: `negative_prompt`/daftar `avoid` boleh memuat istilah kategori terlarang sebagai instruksi pelarangan. Jangan memblokir item hanya karena istilah sensitif muncul di negative prompt yang jelas diawali konteks `no`, `avoid`, `hindari`, atau `tanpa`; filter konten publik/positifnya.

## Keyword Policy

Default config dan database berada di:

- Config: `/root/nusantara-ai-saas/config/content-filter.json`
- Database SQLite keyword negatif: `/root/nusantara-ai-saas/data/content-filter/negative-keywords.db`
- Runner: `/root/nusantara-ai-saas/scripts/content-filter.mjs`

Lingkup default:

```env
NEWS_FILTER_ENABLED=1
NEWS_FILTER_CONFIG_PATH=/root/nusantara-ai-saas/config/content-filter.json
NEWS_FILTER_USE_KEYWORD_DB=1
NEWS_FILTER_KEYWORD_DB_PATH=/root/nusantara-ai-saas/data/content-filter/negative-keywords.db
NEWS_FILTER_BLOCK_CATEGORIES=pornography,pedophilia,violence,religion,politics
NEWS_FILTER_FAIL_CLOSED=1
```

Database menyimpan tabel `filter_keywords` dengan kolom `category`, `term`, `term_hash`, `severity`, `action`, `enabled`, `locale`, `source`, dan audit `filter_audit`. Output publik tetap tidak mencetak istilah negatif mentah; hanya kategori, jumlah match, severity, dan hash term untuk audit internal.

## Output Contract

```yaml
filter_result:
  decision: PASS | BLOCK | REVIEW
  blocked: true | false
  categories:
    - pornography | pedophilia | violence | religion | politics
  matched_terms_redacted:
    - "[REDACTED_TERM]"
  severity: low | medium | high | critical
  reason: "..."
  checked_fields:
    - "topic"
    - "script_narasi"
  safe_for_all_ages: true | false
```

Catatan: jangan menampilkan daftar istilah eksplisit dalam output publik; cukup tampilkan kategori dan jumlah match. Simpan audit internal boleh memakai term hash/redacted.

## Decision Rules

- `BLOCK` jika ada match kategori pedophilia, pornography, politik elektoral, agama/SARA sensitif, gore/kekerasan sadis, atau ajakan/dukungan kekerasan.
- `REVIEW` jika match ambigu, misalnya konteks edukasi/kebijakan umum tetapi mengandung istilah kategori terlarang.
- `PASS` hanya jika tidak ada match terlarang dan konten tetap aman untuk audiens Indonesia semua umur.
- Jika konfigurasi filter tidak bisa dibaca dan `NEWS_FILTER_FAIL_CLOSED=1`, hasil harus `BLOCK`/`REVIEW`, bukan PASS.

## Text Preprocessing

Sebelum pencocokan database keyword negatif, Filter Agent menjalankan praproses teks:
- Unicode NFKC normalization.
- Hapus HTML/tag/entity.
- Hapus zero-width characters.
- Lowercase.
- Normalisasi whitespace.
- Normalisasi leetspeak ringan (`4`→`a`, `3`→`e`, `0`→`o`, dll.).
- Kompres huruf berulang ekstrem.
- Hapus URL dan simbol pemisah berlebih.

Env default:

```env
NEWS_TEXT_PREPROCESS_ENABLED=1
NEWS_TEXT_PREPROCESS_LOWERCASE=1
NEWS_TEXT_PREPROCESS_STRIP_HTML=1
NEWS_TEXT_PREPROCESS_UNICODE=1
NEWS_TEXT_PREPROCESS_WHITESPACE=1
NEWS_TEXT_PREPROCESS_LEETSPEAK=1
NEWS_TEXT_PREPROCESS_ZERO_WIDTH=1
NEWS_TEXT_PREPROCESS_REPEAT_CHARS=1
```

Output publik tidak mencetak teks hasil normalisasi penuh; hanya `preprocessing.changed`, daftar transformasi, dan `normalized_hash`.

## Database Commands

Jalankan dari `/root/nusantara-ai-saas`:

```bash
node scripts/content-filter.mjs --init-db
node scripts/content-filter.mjs --stats
node scripts/content-filter.mjs --preprocess-only --text='teks untuk dicek'
node scripts/content-filter.mjs --text='teks untuk dicek'
```

Exit code:
- `0` = PASS
- `1` = REVIEW
- `2` = BLOCK atau fail-closed

Audit tersimpan di tabel SQLite `filter_audit` tanpa raw text dan tanpa raw terms; hanya hash konten, kategori, jumlah match, severity, dan hash term.

## Storage/Audit

Untuk audit non-secret, simpan ringkasan jika diperlukan ke:

- `/root/nusantara-ai-saas/data/content-filter/filter-log-YYYY-MM-DD.jsonl`

Audit tidak boleh menyimpan credential, signed URL, atau konten eksplisit panjang. Gunakan redaksi/hash untuk term sensitif.

## Reference Notes

- See `references/keyword-db-text-preprocessing.md` for the SQLite negative keyword database schema, text preprocessing behavior, env defaults, commands, and validation pattern.
- See `hermes-agent-orchestration/references/session-2026-05-07-content-filter-and-script-style.md` for the concrete Nusantara-AI cron integration, validator commands, fail-closed behavior, and reporting conventions from the first production setup.

5. **Filtering negative prompts as if they were public content.** Negative prompts and `avoid` lists intentionally contain blocked terms as exclusions. Filter the positive/public prompt and handoff text; do not block solely because the negative prompt says to avoid a forbidden category.

## Verification Checklist

- [ ] `NEWS_FILTER_ENABLED=1`.
- [ ] Config `content-filter.json` tersedia.
- [ ] Filter berjalan sebelum script, sebelum visual/audio, dan sebelum publikasi.
- [ ] `BLOCK` tidak diteruskan ke agent berikutnya.
- [ ] Output tidak menampilkan istilah eksplisit sensitif kecuali path/config internal yang aman.
