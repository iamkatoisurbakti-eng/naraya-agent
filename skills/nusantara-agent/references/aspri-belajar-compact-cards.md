# ASPRI BELAJAR compact class-card UI

Use this when the user asks to remove descriptive metadata from ASPRI BELAJAR material cards, especially duration and video-count labels.

Repo/file:
- `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`

Pattern:
1. Locate the popular class cards under `#popular-classes`.
2. Remove all `<div class="kc-dur">...</div>` blocks from each `.kcard`.
3. Keep the class title (`.kc-name`), action (`.kc-action`), progress (`.kc-prog`), rating (`.kc-star`), and `onclick="openPopularClass('learn-0x')"` intact.
4. Do not remove unrelated uses of “video” in ASPRI VIDEO, chat suggestions, or icons. The target is only ASPRI BELAJAR card metadata like `⏱ 8 jam · 24 video`.
5. Restart `aspri-frontend` after edits so static changes appear immediately.

Verification:
- Extract inline `<script>` blocks and run `node --check` on the combined JS.
- Confirm live HTML contains:
  - `0` occurrences of `<div class="kc-dur">`
  - `0` occurrences of `⏱`
  - `0` matches for `\d+\s*jam\s*·\s*\d+\s*video`
- Check `systemctl is-active aspri-frontend aspri-backend`.
- HTTP-check `http://127.0.0.1:8091/frontend/index.html` and the public URL if needed.

Example quick verification:

```bash
curl -fsS http://127.0.0.1:8091/frontend/index.html -o /tmp/aspri-index.html
python3 - <<'PY'
from pathlib import Path
import re
html = Path('/tmp/aspri-index.html').read_text()
print('kc_dur_divs', html.count('<div class="kc-dur">'))
print('stopwatch_count', html.count('⏱'))
print('kelas_time_video_count', len(re.findall(r'\d+\s*jam\s*·\s*\d+\s*video', html)))
PY
```
