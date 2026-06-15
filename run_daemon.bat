@echo off
REM === Naraya-Agent: daemon 24/7 self-learning + self-evaluation ===
cd /d "%~dp0"
echo Menjalankan Naraya daemon (Ctrl+C untuk berhenti)...
echo Log: logs\daemon.log
python core\naraya_daemon.py
pause
