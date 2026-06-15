---
name: teams-meeting-pipeline
description: Pipeline rapat Microsoft Teams end-to-end — ambil rekaman/transkrip, ringkas, ekstrak keputusan & action item dengan PIC dan tenggat, lalu distribusikan (email/Teams/Slack). Gunakan saat user menyebut rapat Teams, notula, ringkasan meeting, atau follow-up action item.
category: productivity
---

# Teams Meeting Pipeline

Otomasi alur kerja rapat Microsoft Teams dari rekaman sampai tindak lanjut.

## Kapan dipakai
- "ringkas rapat Teams ini", "buat notula", "apa action item dari meeting tadi",
  "kirim follow-up ke peserta", "ekstrak keputusan rapat".

## Tahapan pipeline

1. **Ambil sumber**
   - Transkrip dari Teams (VTT/SRT/teks) atau audio rekaman.
   - Bila audio: pakai tool `speech_to_text` untuk transkripsi.

2. **Bersihkan & strukturkan**
   - Hapus filler, gabungkan giliran bicara per pembicara, beri timestamp.

3. **Ringkas** (gunakan tool `kompres_konteks` / LLM)
   - Ringkasan eksekutif 5–8 kalimat.
   - Poin diskusi utama per topik.

4. **Ekstrak terstruktur** — keluarkan JSON:
   ```json
   {
     "judul": "...", "tanggal": "...", "peserta": ["..."],
     "keputusan": ["..."],
     "action_items": [
       {"tugas": "...", "pic": "...", "tenggat": "YYYY-MM-DD", "prioritas": "tinggi|sedang|rendah"}
     ],
     "risiko": ["..."], "tindak_lanjut": ["..."]
   }
   ```

5. **Distribusi**
   - Kirim ringkasan + action item ke peserta lewat tool `send_message`
     (Teams/Slack/Telegram/webhook) atau email.
   - Opsional: buat reminder/tenggat via `automate_schedule`.

## Praktik baik
- Selalu konfirmasi PIC & tenggat yang ambigu sebelum mengirim.
- Jangan bocorkan transkrip ke pihak di luar daftar peserta.
- Simpan ringkasan ke memori (`add_knowledge`) agar bisa dirujuk rapat berikutnya.

## Integrasi
- STT: `speech_to_text` · Ringkas: `kompres_konteks` · Kirim: `send_message`
- Penjadwalan: `automate_schedule` · Orkestrasi penuh: `orkestrasi_multiagent`.
