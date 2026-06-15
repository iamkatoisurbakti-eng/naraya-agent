# Clean template and send-run notes

Session notes from 2026-05-06:

- Canonical template: `/root/bot_template.html`
- Cleaned layout goals:
  - no left purple sidebar accent
  - no visible description/subtitle under the title
  - dark, minimal card with strong hierarchy
- Patch made in this session:
  - slightly taller card and tighter, cleaner spacing
  - darker badge styling
  - smaller title size with wrap-friendly CSS (`overflow-wrap:anywhere`, `word-break:break-word`, `text-wrap:balance`)
- Verification pattern that worked:
  1. run `npm run gen:viral-news -- --count 1 --dry-run`
  2. inspect the generated PNG with vision
  3. only then rerun a full batch
- Important caveat:
  - long headlines can still clip/ellipsis visually if the source title is too long; prefer shorter headlines or smaller title sizing before large batches
- Telegram send caveat:
  - bulk sends may hit flood control; if one media send fails, wait and resend the failed item instead of restarting the whole batch
