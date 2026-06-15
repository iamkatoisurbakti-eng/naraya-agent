---
name: nusantara-agent
description: Use when working with Nusantara-Agent, the local Indonesian AI agent API, or ASPRI Nusantara app workflows; includes safe local API usage and ASPRI FastAPI/static-app verification conventions.
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [nusantara, indonesia, local-agent, aspri, fastapi, workflow]
    related_skills: [web-app-release-workflow, api-tester]
---

# Nusantara-Agent Skill

Gunakan skill ini ketika user bertanya tentang:
- Nusantara-Agent
- Indonesia
- sejarah Indonesia
- UMKM
- budaya Nusantara
- AI Indonesia
- data/memori Hermes yang sudah dimigrasikan
- agent lokal Nusantara
- ASPRI Nusantara app dan workflow ASPRI

## Local Nusantara-Agent API

Panggil API lokal Nusantara-Agent:

```http
POST http://127.0.0.1:8088/chat
```

Body JSON:

```json
{
  "message": "<pesan user>",
  "user_id": "hermes"
}
```

Gunakan jawaban dari field:

```text
answer
```

Jangan kirim token, password, secret, credential, atau data pribadi sensitif ke API.

## ASPRI Nusantara App local workflow

Gunakan bagian ini ketika task menyentuh:

```text
/root/nusantara-agent/aspri-nusantara-app
```

Struktur umum:
- Backend: FastAPI di `backend/main.py`.
- Frontend: HTML statis mobile-style di `frontend/index.html`.
- Admin: HTML statis di `admin/index.html`.
- Registry fitur: `shared/features.json`.
- Aset PNG lokal ada di root project, termasuk `aspri-video.png` dan `LOGO APP.png`.
- Detail integrasi ASPRI/Nusantara-Agent ada di `references/aspri-app-integration.md`.

### Nusantara-Agent feature integration

Ketika memasukkan Nusantara-Agent ke dalam APP ASPRI:
- Tambahkan feature key `nusantara-agent` ke registry fitur.
- Jika `/feature/{feature}` dipakai, special-case `nusantara-agent` agar memanggil local Nusantara API chat route secara langsung.
- Jika `/workflow/run` dipakai, gunakan route Nusantara chat untuk `feature=nusantara-agent` dan kembalikan output ringkas yang cocok untuk workflow user-facing.
- Update label/home screen bila app ingin menampilkan identitas `NUSANTARA AGENT` di UI.

## Verification Pattern

1. Jika dependency host hilang, gunakan venv lokal, bukan install global:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn httpx pydantic
```

2. Jalankan syntax/build checks:

```bash
. .venv/bin/activate
python -m py_compile backend/main.py scripts/agent_build_app.py autonomous/app_self_improve.py
python scripts/agent_build_app.py
python -c "import fastapi, uvicorn, httpx, pydantic; print('deps ok')"
```

3. Start backend di port 8090:

```bash
. .venv/bin/activate
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8090
```

4. Untuk preview static UI, serve root project di port 8091:

```bash
python3 -m http.server 8091 --bind 0.0.0.0
```

5. Smoke test endpoint utama:

```bash
curl -sS http://127.0.0.1:8090/
curl -sS http://127.0.0.1:8090/features
curl -sS -X POST http://127.0.0.1:8090/workflow/run \
  -H 'Content-Type: application/json' \
  -d '{"feature":"video","template":"shorts_9_16","prompt":"Buat video pendek ASPRI","assets":["aspri-video.png"]}'
curl -sS http://127.0.0.1:8090/workflow/jobs
curl -sS http://127.0.0.1:8090/admin/metrics
curl -I http://127.0.0.1:8091/frontend/index.html
curl -I http://127.0.0.1:8091/admin/index.html
curl -I 'http://127.0.0.1:8091/LOGO%20APP.png'
```

## ASPRI Conventions

- Workflow video request dapat memakai `feature="video"`, `template="shorts_9_16"`, dan asset `aspri-video.png`.
- Frontend/admin sebaiknya derive API base secara dinamis untuk call backend port 8090 ketika static preview jalan di port 8091.
- Pakai `LOGO APP.png` untuk logo aplikasi/admin jika file tersedia.
- Mount/static-serve aset lokal agar PNG bisa diverifikasi via HTTP.
- Untuk inbound WhatsApp asli, lihat `references/whatsapp-webhook-autoreply.md`; POST /whatsapp/webhook adalah path live auto-reply, sedangkan /bantu/whatsapp/autoreply tetap berguna untuk simulasi/manual test.
- Untuk mengubah ASPRI WHATSAPP dari whatsapp-web.js QR menjadi koneksi Meta WhatsApp Business/Cloud API, ikuti `references/aspri-whatsapp-meta-business-redirect.md`: tambahkan `/aspri-whatsapp/meta-config` dan `/aspri-whatsapp/meta-connect`, gunakan direct inline onclick ke meta-connect, dan jangan menunggu async fetch sebelum redirect karena bisa gagal/terlihat tidak responsif di mobile/in-app browser.
- Untuk mengaktifkan/memperbaiki tombol Start/Generate QR ASPRI WHATSAPP berbasis whatsapp-web.js, ikuti `references/aspri-whatsapp-web-qr-activation.md`: expose `latest_qr_data_url`, render QR image di UI, poll status setelah start, dan triage OOM/duplicate Chrome bridge.
- Untuk mengubah ASPRI WHATSAPP dari QR whatsapp-web.js menjadi koneksi/redirect Meta WhatsApp Business Cloud API, ikuti `references/aspri-whatsapp-meta-business-redirect.md`: backend `/aspri-whatsapp/meta-config` + `/meta-connect`, fallback Business Manager bila `WHATSAPP_APP_ID` belum ada, dan jangan echo token/secret.
- Untuk mengaktifkan atau memperbaiki tombol ASPRI WHATSAPP Start / Generate QR, ikuti `references/aspri-whatsapp-web-qr.md`: cek service `aspri-whatsapp` port 8092, expose `latest_qr_data_url` dari `whatsapp-web-service.js`, render QR image di frontend, polling status setelah Start, dan triage OOM/duplikat WA services bila Puppeteer Chrome mati.
- Untuk permintaan ASPRI BELAJAR yang harus langsung membuka ASPRI Chat dan mulai belajar, ikuti `references/aspri-belajar-chat-redirect.md`: class card redirect ke chat, prompt tutor otomatis, chat helper reusable, dan hindari double click binding.
- Untuk ASPRI BELAJAR compact UI, terutama menghapus durasi/jumlah video dari kartu materi, ikuti `references/aspri-belajar-compact-cards.md`: hapus `.kc-dur` saja, pertahankan title/action/progress/rating/onclick, lalu verifikasi live HTML.
- Untuk mengaktifkan/menambahkan modul Beranda ASPRI dengan logo root project (mis. ASPRI BISNIS), ikuti `references/aspri-home-module-activation.md`: tambah card, masukkan id ke `ENABLED_MODULES`, update count/nav, verifikasi asset, dan perhatikan pitfall import backend.
- Untuk membuat/mengaktifkan/merapikan ASPRI BISNIS secara spesifik, ikuti `references/aspri-bisnis-module-ui.md`: gunakan logo `aspri-bisnis.png`, aktifkan `bisnis`, update hitungan modul aktif, bersihkan copy “Debat · Backtest · Validasi 24 Jam Nonstop” bila diminta, dan cek import backend `backend.aspri_chat_agent`.
- Untuk menambahkan foto produk/upload atau sync katalog ASPRI PRODUK ke ASPRI BISNIS, ikuti `references/aspri-bisnis-product-assets-sync.md`: pakai localStorage `aspri_produk_catalog_v1` sebagai source, simpan pilihan bisnis di `aspri_bisnis_assets_v1`, render preview/grid, dan kirim prompt analisis ke ASPRI CHAT tanpa mengirim data URL mentah.
- Untuk menambahkan upload foto produk atau sync produk dari ASPRI PRODUK ke ASPRI BISNIS, ikuti `references/aspri-bisnis-product-assets.md`: frontend-only localStorage, `business-photo`, `business-product-sync`, dynamic asset grid, prompt analisis ke ASPRI CHAT, dan verifikasi `node --check` agar newline JS tidak rusak.
- Untuk permintaan cleanup UI ASPRI kecil seperti menghapus section “Kirim Pesan Test”, label “Analisis Strategi Bisnis”, blok form strategi bisnis, stat counters Beranda (“Modul Aktif”, “Jasa Tersedia”, “AI Powered”), search bar Beranda (“Cari fitur atau layanan...”), menu/halaman “Dompet” termasuk `s-dompet` dan CSS `.dompet-*`, brand copy “X NUSANTARA”, atau melengkapi icon tombol kosong, ikuti `references/aspri-ui-cleanup-and-systemd.md`: hapus blok/teks target saja, audit button/icon, verifikasi source+live count=0, restart frontend, dan cek backend health.
- Untuk melengkapi tombol/icon ASPRI yang terlihat kosong atau belum konsisten, ikuti `references/aspri-button-icon-completion.md`: audit action controls, tambahkan Tabler `<i class="ti ti-*">`, gunakan `innerHTML` untuk state dinamis, lalu verifikasi live. Untuk polishing umum, pakai CSS class-level agar `button/.gen-btn/.analyze-btn/.ic-btn` inline-flex dengan gap seragam, dan buat logo/icon image backgrounds transparan (`.brand-logo`, `.login-logo`, `.asset-icon`, `.mod-logo`, `.product-thumb`) dengan `object-fit: contain` supaya tidak tampak kotak putih/gelap.
- Untuk membuat/mengaktifkan ASPRI KEUANGAN sebagai ledger pemasukan/pengeluaran dengan logo `aspri-keuangan.png`, input ketik, input suara, total pemasukan, total pengeluaran, dan saldo bersih, ikuti `references/aspri-keuangan-ledger-module.md`.
- Untuk membuat/mengaktifkan ASPRI PRODUK sebagai katalog produk dengan logo root project, field nama/deskripsi/harga/gambar/stok, preview gambar, katalog localStorage, dan tombol hapus produk, ikuti `references/aspri-produk-catalog-module.md`.
- Untuk menyambungkan ASPRI BISNIS dengan upload foto produk dan sync dari katalog ASPRI PRODUK, ikuti `references/aspri-bisnis-product-photo-sync.md`: tambah input foto, preview, dropdown produk, sync/clear/analyze buttons, state `aspri_bisnis_assets_v1`, dan verifikasi `node --check`.
- Untuk membuat login panel/auth gate lokal di frontend ASPRI, ikuti `references/aspri-login-panel-auth-gate.md`: login screen harus aktif sebelum HOME, HOME tidak boleh `active`, profile/PIN demo disimpan di browser localStorage, modul digate lewat `nav()`, dan verifikasi HTML live pakai temp file agar `curl | python heredoc` tidak gagal karena stdin terpakai.
- Untuk mengubah ASPRI menjadi Google-only login, ikuti `references/aspri-google-only-login.md`: hapus PIN/register lokal, pakai Google Identity Services, buat `user_id` dari Google `sub`, ganti semua payload API ke `getCurrentAspriUserId()`, dan jangan klaim Google auth live penuh sebelum OAuth Web Client ID dikonfigurasi.
- Untuk menyembunyikan USER-ID/user_id dari dashboard/login namun tetap mengirim `user_id` ke backend, ikuti `references/aspri-user-id-hidden-backend-only.md`: hapus elemen `home-user-id`/`login-user-id` dan teks USER-ID, tetapi pertahankan `generateGoogleUserId()`, `getCurrentAspriUserId()`, dan payload `user_id: getCurrentAspriUserId()`.
- Untuk menyambungkan ASPRI ke domain publik `aspri.nusantara-ai.online`, ikuti `references/aspri-domain-caddy-proxy.md`: edit `/root/nusantara-ai-saas/Caddyfile`, proxy frontend ke host `172.17.0.1:8091`, backend paths ke `172.17.0.1:8090`, reload Caddy container, dan set frontend `apiBase()` same-origin untuk domain tersebut.
- Untuk membuat tombol Start/Generate QR ASPRI WHATSAPP benar-benar menampilkan QR scan di UI, ikuti `references/aspri-whatsapp-qr-activation.md`: proxy `/aspri-whatsapp/*`, service `aspri-whatsapp`, dependency Node `qrcode`, expose `latest_qr_data_url`, render QR image di frontend, polling status, dan triage OOM/duplikat WA bridge.
- Untuk menjadikan ASPRI production live dengan semua modul bisa dipakai, ikuti `references/aspri-production-live-all-modules.md`: audit semua `s-*` screens vs `ENABLED_MODULES`, update home cards 20 modul, update `shared/features.json`, admin feature options, wiring video/emas, restart backend+frontend, dan smoke test domain. Jangan pakai ini bila user sedang meminta dashboard minimal/pruning modul.
- Untuk menghapus/menonaktifkan modul ASPRI dari dashboard/UI/registry/admin, ikuti `references/aspri-module-pruning.md`: hapus card, screen `s-*`, `ENABLED_MODULES`, `shared/features.json`, admin option, bersihkan label tersisa, lalu verifikasi source+live. `references/aspri-module-removal-cleanup.md` adalah referensi terkait/overlap.
- Untuk ASPRI Mobile di Nusantara AI SaaS (`/root/nusantara-ai-saas`, route `/mobile-app` atau `/aspri-mobile`), ikuti `references/nusantara-saas-aspri-mobile-modules.md`: update `src/routes/mobile-agent.ts`, sanitize persisted `data/mobile-agent-state.json` via `readState()`, rewrite conversation `moduleId` fallback, update frontend default `activeModuleId`, lalu build/deploy Docker app dan verify API live.
- Jangan kirim secrets, credentials, tokens, atau data pribadi sensitif ke API lokal Nusantara-Agent.
- Jangan kirim secrets, credentials, tokens, atau data pribadi sensitif ke API lokal Nusantara-Agent.

## Pitfalls

- `python -m uvicorn` bisa gagal dengan `No module named uvicorn`; ini dependency runtime missing, bukan bug source. Buat `.venv`, install deps, lalu retry.
- `ModuleNotFoundError: No module named 'fastapi'` berarti runtime belum terverifikasi.
- ASPRI backend systemd must run from app root with `python -m uvicorn backend.main:app`; if service runs from `backend/` with `uvicorn main:app`, imports like `backend.datarakyat` fail. See `references/aspri-ui-cleanup-and-systemd.md`.
- If adding `sys.path` bootstrapping to `backend/main.py`, keep `from __future__ import annotations` first; otherwise backend crashes with `SyntaxError: from __future__ imports must occur at the beginning of the file`.
- Browser automation bisa gagal karena Chrome profile/socket/process singleton. Jika HTTP checks, asset checks, dan HTML parse lolos, laporkan browser sebagai environment-blocked, bukan app-failed.
- Saat memverifikasi HTML hasil `curl` dengan Python heredoc, jangan pakai `curl ... | python3 - <<'PY'` karena heredoc memakai stdin Python dan pipe bisa memberi `curl: (23) Failure writing output to destination`. Simpan ke temp file lalu jalankan `python3 - "$tmp" <<'PY'`.
- Untuk filename dengan spasi seperti `LOGO APP.png`, test URL encoded path `LOGO%20APP.png`.

## Verification Report Checklist

Saat melapor ke user, ringkas:
- Dependency install/import: pass/fail.
- Syntax/build: pass/fail.
- Backend health/API: pass/fail.
- Workflow run: job id/status jika ada.
- Frontend/admin/static assets: HTTP status/HTML parse.
- Browser automation: pass atau environment-blocked dengan error utama.
- Port/proses yang masih running.
