# ASPRI button/icon completion

Use this reference when the user asks to fill missing/blank button icons in `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`.

## What was learned
- The app uses Tabler icons via `ti ti-*` classes. Prefer existing Tabler icon names over emojis for button/icon consistency.
- Many blank-looking controls are not literally empty `<i>` tags; they are action labels without an icon, such as `promo-cta`, `kc-action`, `popular-complete`, generated news buttons, venue Book/Join buttons, POS remove/payment buttons, and dynamic learning-material completion buttons.
- Dynamic template strings must use `innerHTML` or literal `<i class=...>` inside the template; `textContent` will strip icons.

## Mapping used
- Promo `Chat` -> `<i class="ti ti-message-chatbot"></i>`
- `Buka Kelas` -> `<i class="ti ti-player-play"></i>`
- `Tandai Selesai` / `Tandai selesai` -> `<i class="ti ti-check"></i>`
- Completed states (`Sudah Selesai`, `Selesai`, `Lunas`) -> `<i class="ti ti-circle-check"></i>`
- `Tanya AI Tutor` -> `<i class="ti ti-message-chatbot"></i>`
- Venue `Book` -> `<i class="ti ti-calendar-plus"></i>`
- Venue `Join` -> `<i class="ti ti-user-plus"></i>`
- `Buka Sumber` -> `<i class="ti ti-external-link"></i>`
- `Salin Judul` -> `<i class="ti ti-copy"></i>`
- POS `Hapus` -> `<i class="ti ti-trash"></i>`
- POS `Buat Payment` -> `<i class="ti ti-credit-card"></i>`
- POS `Payment belum siap` -> `<i class="ti ti-alert-circle"></i>`

## Audit script
Run this from the app root after edits:

```bash
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile, os
html = Path('frontend/index.html').read_text()
sus = []
for m in re.finditer(r'<(?:button|a|div)\b([^>]*)>(.*?)</(?:button|a|div)>', html, re.S):
    attrs, inner = m.group(1), m.group(2)
    if any(k in attrs for k in ['gen-btn','create-btn','analyze-btn','ab ','ic-btn','promo-cta','kc-action','news-btn','popular-complete-btn','popular-tutor-btn','pos-paid-btn','learn-done-btn','pos-remove-btn','pos-pay-link-btn']) or m.group(0).startswith('<button'):
        text = ' '.join(re.sub('<[^>]+>', ' ', inner).split())
        has_icon = ('<i ' in inner) or ('<img ' in inner)
        if text and not has_icon and '${' not in text:
            sus.append((html[:m.start()].count('\n') + 1, text[:100]))
print('suspicious iconless controls:', sus)
scripts = re.findall(r'<script>(.*?)</script>', html, flags=re.S)
fd, path = tempfile.mkstemp(suffix='.js')
os.write(fd, ('\n;\n'.join(scripts)).encode()); os.close(fd)
try:
    r = subprocess.run(['node','--check',path], text=True, capture_output=True, timeout=30)
    print('node_check_exit', r.returncode)
    print((r.stdout + r.stderr).strip())
finally:
    os.remove(path)
PY
```

## Transparent icon/image polish
When the user asks to make ASPRI buttons/images/icons cleaner or remove ugly icon backgrounds:
- Add or maintain a central `UI POLISH` CSS block in `frontend/index.html` rather than patching individual buttons one by one.
- Apply consistent button layout to `button`, `.gen-btn`, `.analyze-btn`, `.login-btn`, `.news-btn`, `.product-actions button`, `.ic-btn`, `.ab`, `.promo-cta`, `.qrc`, `.ni`, `.ktab`, `.fchip`, `.vtab`, `.kc-action`: inline-flex/flex alignment, `gap:8px`, `line-height:1.2`, smooth active transform.
- Force button icons transparent: `button i,...{background:transparent!important;}`.
- Make logo/image holders transparent and less boxy: `.brand-logo,.login-logo,.asset-icon,.mod-logo,.product-thumb{background:transparent!important;}` plus `object-fit:contain` for logos/module icons/thumbnails.
- For admin UI, load Tabler icons, add icons to admin buttons, and make `.app-logo` / `.asset img` transparent with `object-fit:contain`.

## Deploy verification
- Restart frontend only for icon-only UI edits: `systemctl restart aspri-frontend`.
- Verify both `frontend/index.html` and `admin/index.html` because ASPRI polish requests often imply the whole app, not just the mobile frontend.
- Verify live HTML from `http://127.0.0.1:8091/frontend/index.html` and `http://127.0.0.1:8091/admin` includes the expected `ti-*` icons / `UI POLISH` CSS.
- Still check backend health (`curl -fsS http://127.0.0.1:8090/`) because the user expects end-to-end production verification.
