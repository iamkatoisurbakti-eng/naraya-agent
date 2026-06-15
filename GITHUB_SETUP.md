# Mempublikasikan Naraya ke GitHub

Ikuti urutan ini agar **tidak ada rahasia** ikut ter-upload.

## 1. Buat paket rilis bersih

```bash
cd "C:\Naraya Agent"
python make_release.py
```
Hasil ada di `release/naraya-agent/` — sudah tanpa `.env`, data pribadi, dan skill berisiko,
serta sudah dipindai kebocoran rahasia (build dibatalkan bila ada).

## 2. Inisialisasi git di folder rilis

```bash
cd release/naraya-agent
git init
git add .
git status            # PASTIKAN .env / *.db / logs/ TIDAK muncul
git commit -m "Naraya-Agent 0.1.0 — rilis open-source awal"
```

## 3. Buat repo di GitHub & push

Opsi A — pakai GitHub CLI:
```bash
gh repo create naraya-agent --public --source=. --remote=origin --push
```

Opsi B — manual:
```bash
# buat repo kosong di github.com lalu:
git branch -M main
git remote add origin https://github.com/<user>/naraya-agent.git
git push -u origin main
```

## 4. Setelah push
- CI (`.github/workflows/ci.yml`) otomatis berjalan: cek sintaks, `doctor`, scan rahasia, lint skill.
- Aktifkan **GitHub Security Advisories** (tab Security) untuk laporan kerentanan privat.
- Tambah topik repo: `ai`, `agent`, `llm`, `indonesia`, `cli`.
- (Opsional) buat rilis tag `v0.1.0`:
  ```bash
  git tag v0.1.0 && git push origin v0.1.0
  ```

## Pengguna lain memakai Naraya
```bash
git clone https://github.com/<user>/naraya-agent.git
cd naraya-agent
python naraya.py install                            # pasang dependensi + daftar perintah global + onboarding
cp core/.env.example .env                           # isi API key
naraya work "Buat REST API katalog produk"          # dari folder mana saja
```
Tanpa venv & tanpa `pip install` manual — Naraya mengurusnya sendiri pada pemakaian pertama.

## PENTING
- Jangan `git init`/push di `C:\Naraya Agent` (root) — masih berisi `.env` dengan rahasiamu.
  Selalu publikasikan dari `release/naraya-agent/`.
- Bila kunci pernah terbagi (mis. lewat chat), **rotasi** di dashboard provider.
