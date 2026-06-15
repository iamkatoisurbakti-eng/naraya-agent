# ASPRI UI Module Cleanup Notes

Use when the user asks to remove, simplify, or production-polish ASPRI app modules in `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`.

Patterns from recent ASPRI cleanup work:
- User prefers production-facing labels. Remove test/debug phrasing such as `Kirim Pesan Test`, `Debat · Backtest · Validasi 24 Jam Nonstop`, visible `24 jam nonstop`, and duration/video copy on class cards when requested.
- For ASPRI BELAJAR compact cards, remove only the `<div class="kc-dur">...</div>` blocks; keep title, action, progress/rating, and `onclick` behavior.
- For ASPRI WHATSAPP, removing the test-send card means deleting the visible workflow-card containing `Kirim Pesan Test`, `wa-to`, `wa-message`, and `wa-send`. Existing JS constants/event listeners can remain guarded by null checks if present.
- For ASPRI BISNIS, simplify labels to production wording: `Analisis Strategi Bisnis`, `Analisis Bisnis`, `Siap menjalankan evaluasi bisnis`, and avoid debate/backtest/24h language in visible UI.
- After edits, run JS extraction check with `node --check`, restart `aspri-frontend`, and verify live HTML no longer contains the removed strings.

Systemd/backend pitfall:
- The backend service may alternate between `WorkingDirectory=/root/nusantara-agent/aspri-nusantara-app` with `python -m uvicorn backend.main:app` and `WorkingDirectory=.../backend` with `uvicorn main:app`.
- If imports fail (`No module named backend` or `No module named aspri_chat_agent`), keep `from __future__ import annotations` at line 1 and make imports robust, or normalize the systemd service to app root + `backend.main:app`.
- Always verify `curl http://127.0.0.1:8090/` after service changes; `systemctl is-active` can briefly report active while the service is crash-looping.