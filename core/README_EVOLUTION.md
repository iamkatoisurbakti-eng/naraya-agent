# Naraya-Agent — Engine Evolusi & Evaluasi (versi nyata)

Dokumen ini menjelaskan mesin self-improvement yang sudah ditulis ulang agar
**benar-benar terukur**, menggantikan versi lama yang memalsukan peningkatan
(`score_after = score_before + 5`) dan benchmark berbasis pencocokan string.

## Komponen

| File | Peran |
|------|-------|
| `llm.py` | Wrapper LLM terpusat. Model & provider dari env (`NARAYA_MODEL`, `OPENAI_BASE_URL`). Aman saat offline (`LLMUnavailable`). |
| `eval/tasks.json` | Dataset benchmark: 8 task (reasoning, instruction-following, planning, structured output, bahasa, faktual, safety, ringkasan). |
| `benchmark_engine.py` | Harness eval nyata: skor deterministik (regex `checks`, 0-50) + LLM-judge (rubric, 0-50). Simpan tiap run ke `benchmark_runs`. |
| `prompt_store.py` | Menyimpan "system prompt terbaik" yang persisten (`data/prompts/system_prompt.txt`) + riwayat versi (`prompt_versions`). |
| `evolution_engine.py` | Optimasi prompt: usul kandidat → uji → terapkan **hanya jika skor naik > MIN_DELTA**. Angka before/after asli ke `evolution_history`. |
| `self_play.py` | Debat multi-agent → sintesis → **dinilai judge**; hanya insight skor ≥ 70 yang disimpan. Log ke `self_play_runs`. |
| `autonomous_evolution.py` | Siklus otonom: benchmark → refine memory → evolve → self-play. Tidak ada efek samping saat di-import. |

## Konfigurasi (.env / environment)

```
OPENAI_API_KEY=...            # atau NARAYA_API_KEY
NARAYA_MODEL=gpt-4.1-mini  # model utama
NARAYA_JUDGE_MODEL=...      # opsional, default = NARAYA_MODEL
OPENAI_BASE_URL=...           # opsional, untuk provider OpenAI-compatible
NARAYA_EVO_INTERVAL_MIN=60 # interval loop otonom (menit)
```

## Cara pakai (jalankan dari root project)

```bash
# 1) ukur skor agen sekarang
PYTHONPATH=core python3 core/benchmark_engine.py

# 2) satu siklus evolusi terukur (uji & terapkan prompt lebih baik)
PYTHONPATH=core python3 core/evolution_engine.py

# 3) self-play menghasilkan insight tersaring
PYTHONPATH=core python3 core/self_play.py

# 4) siklus otonom sekali jalan / loop terjadwal
PYTHONPATH=core python3 core/autonomous_evolution.py --once
PYTHONPATH=core python3 core/autonomous_evolution.py
```

## Cara membaca hasil

- `data/prompts/system_prompt.txt` — prompt aktif terbaik saat ini.
- Tabel `prompt_versions` — riwayat tiap versi prompt + skornya + mana yang aktif.
- Tabel `benchmark_runs` — tiap evaluasi (skor, detail per task).
- Tabel `evolution_history` — before/after tiap siklus (improvement asli, applied 0/1).
- `logs/evolution_cycles.log` — ringkasan tiap siklus otonom.

## Sifat penting

- **Tidak ada peningkatan palsu.** Prompt baru hanya menggantikan yang lama bila
  skor benchmark benar-benar naik melebihi ambang (`MIN_DELTA`, default 1.0 poin).
- **Offline-safe.** Tanpa API key, engine mengembalikan status `offline` tanpa crash
  (berguna untuk CI / dry-run).
- **Provider-agnostic.** Ganti model/provider lewat env tanpa mengubah kode.
