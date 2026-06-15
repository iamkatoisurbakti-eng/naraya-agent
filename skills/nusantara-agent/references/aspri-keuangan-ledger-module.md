# ASPRI KEUANGAN Ledger Module

Use when the user asks to create/activate ASPRI KEUANGAN with logo `aspri-keuangan.png` and simple income/expense tracking.

## Goal
Create a production-facing ASPRI KEUANGAN module where users can:
- add `Pemasukan` by typing
- add `Pengeluaran` by typing
- see `Total Pemasukan`
- see `Total Pengeluaran`
- see `Saldo Bersih`
- add transactions with voice input using Web Speech API when the browser supports it

## Frontend source
Main file:

```text
/root/nusantara-agent/aspri-nusantara-app/frontend/index.html
```

Logo asset:

```text
/root/nusantara-agent/aspri-nusantara-app/aspri-keuangan.png
```

## Implementation pattern
1. Add/activate a home card:
   - class: `mc-keuangan aspri-keuangan-card`
   - onclick: `nav('keuangan')`
   - logo: `../aspri-keuangan.png`
   - copy: concise, e.g. `Catat pemasukan dan pengeluaran dengan ketik atau suara`
2. Update active module count (`4` -> `5`, `4 aktif` -> `5 aktif` if matching current app state).
3. Add `keuangan` to `ENABLED_MODULES`.
4. Prefer replacing older placeholder/evaluation UI in `s-keuangan` with a ledger UI:
   - logo/hero block
   - totals: `finance-income-total`, `finance-expense-total`, `finance-net-total`
   - form fields: `finance-entry-type`, `finance-entry-amount`, `finance-entry-note`
   - buttons: `finance-add-income`, `finance-add-expense`, `finance-voice`
   - list container: `finance-ledger`
5. Use `localStorage` for the lightweight per-browser ledger unless the user explicitly asks for server persistence.
   - Stable key used in session: `aspri_keuangan_transactions_v1`
6. Voice input:
   - Use `window.SpeechRecognition || window.webkitSpeechRecognition`.
   - Language: `id-ID`.
   - Parse examples like:
     - `pemasukan dua juta dari penjualan`
     - `pengeluaran lima ratus ribu beli bahan baku`
     - `beli bahan baku 500 ribu`
   - If unsupported, show a status message and keep typed input flow working.
7. Use existing `formatMoney` helper for display; totals should update immediately after add.

## Useful parse helpers
- Numeric amounts: `2500000`, `2 juta`, `500 ribu`, `500 rb`.
- Indonesian words: at least handle `satu`, `dua`, `tiga`, `empat`, `lima`, `sepuluh`, `sebelas`, phrase keys like `'dua belas'`, `'dua puluh'`, etc.
- Quote multi-word object keys in JS object literals (`'dua belas': 12`), otherwise `node --check` fails with `Unexpected identifier`.

## Verification
Run source checks:

```bash
cd /root/nusantara-agent/aspri-nusantara-app
python3 - <<'PY'
from pathlib import Path
import re, subprocess, tempfile, os
root=Path('.')
html=Path('frontend/index.html').read_text()
checks={
 'asset_exists': (root/'aspri-keuangan.png').exists(),
 'home_card': 'aspri-keuangan-card' in html and '../aspri-keuangan.png' in html,
 'enabled': "'keuangan'" in html,
 'income_button': 'finance-add-income' in html,
 'expense_button': 'finance-add-expense' in html,
 'voice_button': 'finance-voice' in html and 'SpeechRecognition' in html,
 'totals': all(x in html for x in ['finance-income-total','finance-expense-total','finance-net-total']),
}
for k,v in checks.items(): print(k, 'PASS' if v else 'FAIL')
scripts=re.findall(r'<script>(.*?)</script>', html, flags=re.S)
fd,path=tempfile.mkstemp(suffix='.js')
os.write(fd, ('\n;\n'.join(scripts)).encode()); os.close(fd)
try:
    r=subprocess.run(['node','--check',path], capture_output=True, text=True, timeout=30)
    print('node_check_exit', r.returncode)
    print((r.stdout+r.stderr).strip())
finally:
    os.remove(path)
PY
```

Deploy/health:

```bash
systemctl restart aspri-frontend
curl -fsS http://127.0.0.1:8091/frontend/index.html -o /tmp/aspri-index.html
curl -sS -I http://127.0.0.1:8091/aspri-keuangan.png | head
curl -fsS http://127.0.0.1:8090/
systemctl is-active aspri-backend aspri-frontend
```

## Pitfalls
- If `curl` immediately after frontend restart fails once with connection refused, retry after 1-2 seconds; service is still starting.
- Web Speech API may require HTTPS or browser permission in real browsers. Keep typed input as the guaranteed path.
- Existing ASPRI code has global `.ktab` click behavior. If adding filter tabs inside `s-keuangan`, add a scoped handler (`#s-keuangan .ktab`) to set a local filter and re-render the ledger.
