# Session note: 95+ threshold for single prompt

Updated behavior:
- Single-news / single-prompt mode must only proceed if the selected item score is >= 95.
- The score is stored in `manifest.json` from `genz-news.ts` and consumed by `news-pipeline.ts` before image/video generation.
- If no item clears the threshold, fail early with a clear error instead of generating partial assets.

Related guardrails:
- Telegram send is skipped per item when required image/video files are missing.
- Image default is Ark.
- Video default is Ark.
