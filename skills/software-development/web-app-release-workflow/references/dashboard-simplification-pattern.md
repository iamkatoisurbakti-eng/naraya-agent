# Dashboard simplification pattern

Session learning: when users ask to make the app easier to use, simplify the authenticated dashboard and studio UI without removing capabilities.

## What changed successfully
- Renamed dashboard nav items to outcome-first labels:
  - Beranda, Riwayat, Gambar, Video, Musik, Suara, Potong Video, Berita, Chat, Admin
- Shortened the top CTA from `Topup Credit` to `Isi Kredit`.
- Removed a decorative desktop search box from the top bar because it added clutter without a clear action.
- Reframed Quick Create into direct feature chips:
  - Chat, Gambar, Video, Musik, Voice, Clipper
- Shortened studio copy to reduce cognitive load:
  - `Buat cepat`, `Prompt dulu`, `Hasil`
- Renamed technical labels to user language:
  - Model, Rasio, Frame awal/akhir, Gambar referensi, Video referensi, Audio referensi, Sapaan awal, Bahasa
- Kept advanced controls available, but made the default flow prompt-first.

## Rule of thumb
- Prefer progressive disclosure over removing features.
- Keep the default path to one prompt and one primary button.
- Hide or defer technical controls until the user asks for them.
- Use build verification after the UI copy/layout pass (`npm run build:web`).
