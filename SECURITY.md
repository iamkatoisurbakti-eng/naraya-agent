# Kebijakan Keamanan

## Melaporkan kerentanan
Jangan buka issue publik untuk kerentanan keamanan. Laporkan secara privat lewat
**GitHub Security Advisories** (tab Security → Report a vulnerability) atau email
maintainer. Kami berusaha merespons dalam 72 jam.

## Rahasia (API key, token, password)
- Semua rahasia hanya di `.env` (sudah di-`.gitignore`). **Jangan pernah commit `.env`.**
- Bila sebuah kunci pernah terlanjur ter-commit/terbagi, **rotasi (ganti) segera**.
- Sebelum publikasi, jalankan `python make_release.py` — membuat paket bersih dan
  memindai kebocoran rahasia (build dibatalkan bila ada).
- CI menjalankan `secrets-scan` pada setiap push/PR.

## Kapabilitas berisiko
`terminal` dan `eksekusi_python` menjalankan perintah/kode di mesin pengguna.
Jalankan Naraya hanya pada mesin/akun yang kamu percaya. Skill kelas
red-teaming/jailbreak/carding tidak diterima di repo ini.

## Praktik aman pengguna
- Tinjau perintah sebelum mengeksekusi pada data/akun penting.
- Gunakan akun/kunci API dengan hak seminimal mungkin.
