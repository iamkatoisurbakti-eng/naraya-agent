# Berkontribusi ke Naraya-Agent

Terima kasih ingin membuat Naraya makin pintar! Ada tiga jalur kontribusi utama.

## 1. Tambah skill (skill hub)

Skill = pengetahuan/prosedur yang otomatis dicocokkan ke tugas. Strukturnya:

```
skills/<kategori>/<nama-skill>/SKILL.md
```

`SKILL.md` diawali frontmatter:

```markdown
---
name: nama-skill
description: Satu kalimat kapan skill ini dipakai dan apa manfaatnya.
category: kategori
---

# Judul Skill
Isi: langkah, contoh, perintah, batasan.
```

Checklist PR skill:
- [ ] `name` & `description` jelas (description menentukan pencocokan otomatis).
- [ ] Tidak memuat rahasia, data pribadi, atau instruksi ilegal/berbahaya.
- [ ] Diuji: `python naraya.py skills "<kata kunci>"` memunculkan skill-mu.

> Skill berisiko (mis. kategori `red-teaming`, jailbreak, carding) **tidak** diterima
> di repo utama dan otomatis dikecualikan oleh `make_release.py`.

## 2. Sumbang dataset evaluasi & prompt

Kualitas Naraya diukur lewat `core/eval/tasks.json`. Tambah task baru bila kamu punya
kasus uji yang bagus:

```json
{
  "id": "id_unik",
  "category": "reasoning|coding|safety|...",
  "prompt": "pertanyaan/tugas",
  "checks": ["regex1", "regex2"],
  "min_checks": 1,
  "rubric": "kriteria penilaian untuk LLM-judge"
}
```

Evolusi prompt (`core/evolution_engine.py`) hanya menerapkan perubahan bila skor
benchmark **benar-benar naik**, jadi task yang baik langsung meningkatkan kualitas semua.

## 3. Kode (engine & tools)

- Modul inti ada di `core/`. Gaya: ringkas, dependensi opsional di-import lazy,
  selalu **offline-safe** (jangan crash bila tak ada API key).
- Tambah tool baru: tulis fungsi di `core/agent_tools.py` + bungkus `@function_tool`
  di `core/rag_agent.py` + masukkan ke `ALL_TOOLS`.
- Tambah agen orkestrasi: lihat `AGENTS`/`PHASES` di `core/multi_agent.py`.
- Sebelum PR: `python -m py_compile core/*.py naraya.py` dan, bila relevan,
  `python naraya.py eval`.

## Aturan dasar

- Jangan pernah commit rahasia. `.env` sudah di-`.gitignore`; pakai `core/.env.example`.
- Sebelum rilis/publik: `python make_release.py` (membuat paket bersih + memindai rahasia).
- Bahasa Indonesia diutamakan untuk prompt/dokumentasi pengguna; kode boleh Inggris.
- Dengan berkontribusi, kamu setuju kontribusimu dilisensikan di bawah MIT.
