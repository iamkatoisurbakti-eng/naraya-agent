# Deploy Naraya-Agent di VPS (Linux)

Panduan untuk Ubuntu/Debian. Cocok untuk menjalankan **gateway Telegram** dan
**daemon self-learning 24/7** secara persisten.

## 1. Prasyarat

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
```

## 2. Ambil kode

Opsi A — dari GitHub (setelah kamu push paket rilis bersih):
```bash
git clone https://github.com/<user>/naraya-agent.git
cd naraya-agent
```

Opsi B — unggah dari komputermu (tanpa GitHub):
```bash
# di komputermu (PowerShell), buat dulu paket bersih lalu kirim:
#   python make_release.py
#   scp -r release/naraya-agent <user>@<ip-vps>:~/
# lalu di VPS:
cd ~/naraya-agent
```

> Jangan unggah `.env` lamamu ke VPS publik. Buat `.env` baru di VPS dan isi kunci di sana.

## 3. Install (otomatis)

```bash
bash install.sh
# atau: python3 naraya.py install
```

Isi kunci API:
```bash
cp core/.env.example .env   # bila belum
nano .env                   # set OPENAI_API_KEY / NARAROUTER_API_KEY / dll, NARAYA_PROVIDER
python3 naraya.py doctor    # harus: API key ada ✓
```

## 4. Coba

```bash
python3 naraya.py work "Buat REST API katalog produk"
python3 naraya.py chat
```

## 5. Jalan 24/7 dengan systemd

### a) Gateway Telegram (balas pesan via tools)
`/etc/systemd/system/naraya-gateway.service`:
```ini
[Unit]
Description=Naraya Telegram Gateway
After=network-online.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/home/YOUR_USER/naraya-agent
ExecStart=/usr/bin/python3 naraya.py gateway telegram
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### b) Daemon self-learning + self-evaluation
`/etc/systemd/system/naraya-daemon.service`:
```ini
[Unit]
Description=Naraya Self-Learning Daemon
After=network-online.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/home/YOUR_USER/naraya-agent
ExecStart=/usr/bin/python3 naraya.py daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Aktifkan:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now naraya-gateway naraya-daemon
systemctl status naraya-gateway        # cek
journalctl -u naraya-gateway -f         # lihat log realtime
```

> `.env` dibaca otomatis oleh aplikasi (python-dotenv) dari `WorkingDirectory`,
> jadi tak perlu `EnvironmentFile`.

## 6. Update versi
```bash
cd ~/naraya-agent && git pull       # bila dari GitHub
python3 naraya.py install           # pasang dependensi baru bila ada
sudo systemctl restart naraya-gateway naraya-daemon
```

## 7. Tanpa systemd (cepat, sesi terminal)
```bash
# tetap jalan setelah logout:
nohup python3 naraya.py gateway telegram > gateway.log 2>&1 &
nohup python3 naraya.py daemon > daemon.log 2>&1 &
# atau pakai tmux/screen
```

## Keamanan VPS
- Buat user non-root untuk menjalankan Naraya (jangan root).
- `chmod 600 .env` agar kunci tak terbaca user lain.
- Batasi akses Telegram: isi `TELEGRAM_ALLOWED_USERS` (jangan `NARAYA_GATEWAY_ALLOW_ALL=true`).
- Ingat: `terminal`/`eksekusi_python` menjalankan perintah di VPS — pakai user terbatas.
