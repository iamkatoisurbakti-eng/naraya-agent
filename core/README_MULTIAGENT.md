# Naraya-Agent — Multi-Agent Orchestration

Setiap pekerjaan nyata dijalankan sebagai **pipeline 14 agen spesialis** (`core/multi_agent.py`).
Output tiap agen dioper (handoff) ke agen berikutnya lewat konteks berjalan yang dikompres.

## Urutan pipeline

`memory → planner → research → architect → design → debate → backend → frontend → coding → testing → security → qa → documentation → deployment` → (memory menyimpan ringkasan)

| Agen | Peran |
|------|------|
| Memory | kumpulkan & ringkas konteks/asumsi |
| Planner | pecah goal jadi langkah |
| Research | kumpulkan fakta (boleh web_search) |
| Architect | rancang arsitektur & teknologi |
| Design | rancang UX/UI & alur |
| Debate | adu pro-kontra, pilih opsi terbaik |
| Backend | API, model data, logika server |
| Frontend | komponen UI & integrasi |
| Coding | tulis kode konkret |
| Testing | rencana & kasus uji |
| Security | risiko & mitigasi keamanan |
| QA | tinjauan kualitas menyeluruh |
| Documentation | dokumentasi ringkas |
| Deployment | langkah deploy & rollback |

## Mode eksekusi

- **parallel** (default): agen tak-saling-bergantung dalam satu fase dijalankan SERENTAK (ThreadPool) → lebih cepat (~1,5× pada 14 agen).
- **sequential**: tiap agen berurutan, melihat penuh hasil agen sebelumnya (handoff maksimal).

Fase paralel: `[memory] → [planner] → [research] → [architect|design] → [debate] → [backend|frontend] → [coding] → [testing|security|qa] → [documentation|deployment]`.

## Cara pakai

```python
# dari kode
from multi_agent import work, orchestrate
print(work("Buat aplikasi to-do list", mode="parallel"))   # laporan teks (default paralel)
hasil = orchestrate("...", mode="sequential")               # dict terstruktur
hasil = orchestrate("...", agents=["testing","security","qa"], mode="parallel")  # subset agen

# dari CLI
python core/multi_agent.py "Buat REST API katalog produk"          # paralel
python core/multi_agent.py --seq "Buat REST API katalog produk"    # sequential

# lewat agen utama (otomatis dipakai untuk tiap pekerjaan nyata)
from agent_core import work
work("Rancang dan bangun fitur login", mode="parallel")
```

Parameter `orchestrate(goal, agents=None, mode="sequential", max_workers=4, verbose=False, revise=False, max_revisions=2, on_event=None)`.
Tool agen: `orkestrasi_multiagent(goal, mode="parallel", revise=True)`.

## Loop revisi otomatis (`revise=True`, default di work/tool)

Setelah fase review, temuan **Testing/Security/QA** dinilai (LLM-judge bila ada API key,
else heuristik kata kunci). Jika ada isu yang harus diperbaiki:

`temuan → Coding memperbaiki (coding#rev1) → review ulang (testing/security/qa #rev1) → cek lagi`

Berulang sampai bersih atau mencapai `max_revisions`. Setiap putaran tercatat di
`result["revisions"]` dan ringkasannya tampil di laporan. CLI: tambahkan `--no-revise` untuk mematikan.

## Streaming progress

Beri callback `on_event(ev)` ke `orchestrate`/`work`. Tiap agen memancarkan event
`{"agent","status","round","preview","t"}` dengan status `start`/`done` (dan `review`
untuk titik keputusan revisi). Semua event juga tersimpan di `result["events"]`.

```python
def show(ev): print(f"[{ev['status']}] {ev['agent']} rev{ev['round']}")
work("Buat REST API", on_event=show)            # progress real-time
python core/multi_agent.py "Buat REST API"      # streaming + revisi di terminal
```

## Hemat token (ringkasan berjalan)

Antar-agen tidak lagi mengoper konteks penuh. Orkestrator menjaga **ringkasan berjalan**
yang dipadatkan ke `context_budget` (default 700 karakter) — digest 1 baris per agen,
dikompres saat melebihi budget. Output penuh tiap agen tetap tersimpan di `report` untuk
laporan akhir, tapi yang dialirkan ke agen berikutnya hanya ringkasannya. Atur via
`orchestrate(..., context_budget=700)`.

## Agen dinamis (otomatis bila perlu)

`dynamic=True` (default): sebelum eksekusi, orkestrator menanyakan ke LLM apakah pekerjaan
butuh agen spesialis TAMBAHAN (mis. Data Engineer, ML, DevOps). Bila ya, agen ad-hoc dibuat
dan disisipkan sebagai fase paralel setelah `research`. Dimatikan dengan `dynamic=False`
atau saat memakai subset `agents=[...]`.

## Selalu pakai skills

Tiap agen menerima blok **SKILLS RELEVAN** dari `skills_index.py` (dicocokkan dari registry
skill / `skills/**/SKILL.md` berdasar goal), dengan instruksi memanfaatkannya bila cocok.

## Self-learning & self-evaluation 24/7 (daemon)

`core/naraya_daemon.py` menjalankan dua loop terjadwal:
- **Self-evaluation** tiap `NARAYA_EVAL_INTERVAL_MIN` (default 60 mnt): benchmark nyata → catat skor.
- **Self-learning** tiap `NARAYA_LEARN_INTERVAL_MIN` (default 180 mnt): refine memori → evolusi
  prompt (hanya diterapkan bila skor naik) → self-play → reindex skills.

```bash
python core/naraya_daemon.py            # jalan 24/7
python core/naraya_daemon.py --once     # uji sekali
run_daemon.bat                          # Windows
```
Offline-safe: tanpa API key, loop mencatat `offline` dan menunggu. Log: `logs/daemon.log`.

## Sifat penting
- **Selalu multi-agen**: master agent diinstruksikan menjalankan `orkestrasi_multiagent`
  untuk setiap pekerjaan nyata; obrolan ringan tetap dijawab langsung.
- **Offline-safe**: tanpa `OPENAI_API_KEY`, tiap agen mengembalikan status `offline`
  tanpa crash; struktur laporan tetap utuh.
- **Tercatat**: tiap run disimpan ke `data/orchestration_runs.db`; ringkasan akhir
  juga masuk memori jangka panjang (`long_term_knowledge`).
- **Hemat token**: konteks antar-agen dikompres otomatis.
