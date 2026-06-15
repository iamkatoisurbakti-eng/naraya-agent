@echo off
REM === Naraya-Agent (Windows): pasang dependensi + daftar perintah global + onboarding ===
cd /d "%~dp0"
echo.
echo Memasang Naraya (sekali jalan)...
python naraya.py install
echo.
echo Selesai. Isi kunci API di .env (lihat core\.env.example), lalu dari folder mana saja:
echo    naraya work "tugas pertama kamu"
pause
