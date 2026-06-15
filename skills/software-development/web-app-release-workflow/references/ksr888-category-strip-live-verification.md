# KSR888 category-strip live verification

Session pattern:
- When changing the KSR888 desktop category strip / nav row, verify the rendered live HTML directly at `https://ksr888.online/dekstop/index.php`.
- Use a browser-like fetch and grep the HTML for the expected visible labels and `category-strip` container before declaring success.
- Confirm the `ksr888-web` container is running with `docker compose ps` and that the page is reachable over HTTPS.

Example probe used in this session:
```bash
curl -s https://ksr888.online/dekstop/index.php \
  | grep -n 'category-strip\|SLOTS\|LIVE GAMES\|SPORTS\|CASINO\|P2P\|LOTRE\|SABUNG AYAM\|TEMBAK IKAN\|E-GAMES\|PROMOSI\|HOT' \
  | head -40

docker compose ps
```

Observed output:
- The live HTML contained the expected strip labels and HOT badges.
- `ksr888-web` was up and mapped on port 80 inside the Compose stack.

Use this as the fast-path proof for banner/category-strip changes when browser screenshots are unnecessary or blocked.