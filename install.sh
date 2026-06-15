#!/usr/bin/env bash
# === Naraya-Agent: installer untuk Linux/VPS ===
set -e
cd "$(dirname "$0")"

PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
  echo "Python3 tidak ditemukan."
  echo "Ubuntu/Debian: sudo apt update && sudo apt install -y python3 python3-pip python3-venv git"
  exit 1
fi

echo "Memasang Naraya-Agent dengan $PY ..."
"$PY" naraya.py install

if [ ! -f .env ] && [ -f core/.env.example ]; then
  cp core/.env.example .env
  echo "Dibuat .env dari contoh — isi API key kamu (nano .env)."
fi

echo
echo "Selesai. Berikutnya:"
echo "  nano .env                       # isi OPENAI_API_KEY / provider lain"
echo "  $PY naraya.py doctor            # cek koneksi"
echo "  $PY naraya.py work \"tugas pertama\""
