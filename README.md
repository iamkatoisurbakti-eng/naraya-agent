# Naraya-Agent 🇮🇩

<!-- Ganti `your-org` dengan username/organisasi GitHub-mu setelah push. -->
[![CI](https://github.com/your-org/naraya-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/naraya-agent/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Providers](https://img.shields.io/badge/providers-7-success.svg)](core/README_PROVIDERS.md)
[![Skills](https://img.shields.io/badge/skills-500%2B-orange.svg)](skills/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Agen AI lokal berbahasa Indonesia yang berjalan di terminal. Naraya menggabungkan
**orkestrasi multi-agen**, **multi-provider LLM**, **self-learning 24/7**, ratusan
**skills**, dan kumpulan **tools** (web, kode, computer-use, MCP) dalam satu paket
open-source.

> Status: **research preview / 0.1.0** — kontribusi sangat diterima.

## 📌 Ringkasan fitur

| Area | Kemampuan |
|------|-----------|
| 🤝 Multi-agen | 14 agen spesialis + agen dinamis · mode paralel · loop revisi otomatis · streaming progress · konteks hemat token |
| 🔌 Multi-provider | NaraRouter · OpenAI · Anthropic · OpenRouter · Kilo Code · Custom direct/endpoint |
| 🧠 Self-improve | benchmark terukur · evolusi prompt (hanya diterapkan bila skor naik) · self-play · daemon 24/7 |
| 📚 Skills | 500+ skill, dicocokkan otomatis ke tiap tugas |
| 🛠️ Tools | web search/browse · browser otomatis · eksekusi kode · terminal · vision · image-gen · voice · messaging · Home Assistant · MCP |
| 💻 CLI | `chat` · `work` · `provider` · `eval` · `learn` · `daemon` · `skills` · `doctor` |
| 🔒 Aman | rahasia hanya di `.env` · rilis bersih ter-scan · offline-safe |

## ✨ Fitur

- **Orkestrasi multi-agen** — tiap pekerjaan melewati 14 agen spesialis (memory,
  planner, research, architect, design, debate, backend, frontend, coding, testing,
  security, qa, documentation, deployment) + **agen dinamis** bila dibutuhkan.
  Mode **paralel** (cepat), **loop revisi otomatis** (temuan QA/Security → perbaikan),
  **streaming progress**, dan **konteks hemat token**.
- **Multi-provider** — NaraRouter, OpenAI, Anthropic, OpenRouter, Kilo Code, serta
  Custom direct/endpoint (OpenAI-compatible). Ganti lewat satu perintah.
- **Self-learning & self-evaluation 24/7** — daemon yang mengukur kualitas (benchmark)
  dan mengevolusi prompt secara **terukur** (hanya diterapkan bila skor naik) + self-play.
- **500+ skills** — pustaka pengetahuan/prosedur yang dicocokkan otomatis ke tiap tugas.
- **Tools** — web search/browse, browser otomatis (Playwright), eksekusi kode, terminal,
  vision, image-gen, voice (TTS/STT), messaging, Home Assistant, MCP client, dan lain-lain.

## 🚀 Instalasi

Butuh Python 3.9+. **Tidak perlu pip install manual** — Naraya memasang dependensinya
sendiri saat pertama dijalankan.

```bash
git clone https://github.com/your-org/naraya-agent.git
cd naraya-agent
python naraya.py install      # pasang dependensi + daftarkan perintah global + onboarding
```

Setelah `install` selesai, perintah **`naraya`** tersedia dari folder **mana saja** —
tak perlu `cd` lagi:

```bash
naraya work "Buat REST API katalog produk"
naraya chat
```

Windows: bisa juga klik dua kali `install_tools.bat`.
Perintah lain (`work`, `chat`, `eval`, ...) juga otomatis memasang dependensi pada
pemakaian pertama. Untuk memasang ulang: `python naraya.py install`.
(Opsional, bila kamu lebih suka isolasi: `python -m venv .venv` lalu aktifkan sebelum menjalankan.)

## 🔑 Konfigurasi provider

```bash
cp core/.env.example .env          # lalu isi salah satu API key
python naraya.py provider          # lihat status semua provider
python naraya.py provider openai   # pilih provider aktif
python naraya.py provider --test   # uji koneksi nyata
```

Contoh `.env` minimal:

```
NARAYA_PROVIDER=openai
OPENAI_API_KEY=sk-...
NARAYA_MODEL=gpt-4.1-mini
```

NaraRouter, OpenRouter, Kilo Code, Anthropic, dan endpoint custom didukung —
lihat `core/README_PROVIDERS.md`.

## 🖥️ Pemakaian

```bash
python naraya.py doctor                       # cek deps, provider, key
python naraya.py chat                          # obrolan interaktif
python naraya.py work "Buat REST API katalog produk"   # orkestrasi multi-agen
python naraya.py work "..." --seq --no-revise --budget 700
python naraya.py eval                           # benchmark sekali
python naraya.py learn                          # satu siklus self-learning
python naraya.py daemon                         # self-learning + self-eval 24/7
python naraya.py skills "deployment"            # cari skill relevan
```

Setelah `pip install -e .`, semua perintah di atas bisa dipanggil sebagai `naraya ...`.

## 🧠 Bagaimana Naraya menjadi makin pintar

1. **Self-learning lokal** — tiap instance belajar dari pemakaiannya: evolusi prompt
   terukur + memori jangka panjang + self-play (lihat `core/README_MULTIAGENT.md`,
   `core/README_EVOLUTION.md`).
2. **Skill hub komunitas** — tambahkan skill baru (folder `skills/<kategori>/<nama>/SKILL.md`)
   dan kirim PR; pustaka tumbuh untuk semua pengguna.
3. **Berbagi eval & prompt** — sumbang task evaluasi (`core/eval/tasks.json`) agar
   peningkatan kualitas terukur dan adil.

Lihat **CONTRIBUTING.md**.

## 📂 Struktur

```
naraya.py              CLI utama
core/                  mesin: llm, providers, multi_agent, tools, evolusi, daemon
core/eval/tasks.json   dataset benchmark
skills/                pustaka skills (kategori/skill/SKILL.md)
make_release.py        pembuat paket rilis bersih (tanpa rahasia)
```

## 🔒 Keamanan & privasi

- Kunci API hanya dibaca dari `.env` (di-`.gitignore`, tidak pernah di-commit).
- `terminal` & `eksekusi_python` adalah kapabilitas kuat — jalankan di mesin sendiri.
- Sebelum mempublikasi, jalankan `python make_release.py` untuk membuat paket bersih
  yang otomatis mengecualikan rahasia, data pribadi, dan skill berisiko.

## 📜 Lisensi

MIT — lihat [LICENSE](LICENSE).
