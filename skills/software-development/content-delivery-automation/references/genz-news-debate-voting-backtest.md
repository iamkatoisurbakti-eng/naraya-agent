# Gen-Z News Debate/Vote/Backtest Recipe

Session-proven notes for `/root/nusantara-ai-saas/scripts/genz-news.ts`.

## What changed
- Source priority: Berita Indo API multi-source first, then fallback legacy feeds if needed.
- Candidate normalization now tolerates multiple payload shapes, so the selector can rank items from different sources together.
- Ranking is no longer single-pass freshness only. It combines:
  - debate judges (viral, visual, safety, clarity)
  - vote weighting across judges
  - backtest against local history
  - final score + freshness tie-break

## Practical algorithm
1. Fetch candidates from all allowed sources.
2. Normalize into a shared item shape.
3. Build a story key so repeated items can be compared across runs.
4. Run judge-style scoring:
   - viral: clickability / shareability
   - visual: card suitability
   - safety: filter risky content
   - clarity: short-title readability
5. Turn judge outputs into a vote map.
6. Mix vote total with freshness and a backtest score.
7. Sort descending and pick the top item(s).

## Backtest notes
- Backtest is only meaningful after history exists.
- With a thin history file, overlap metrics may be 0.000 even when the pipeline works.
- Save each run’s winning story key to local history so future runs can compare against it.

## Render pitfall
- The Gen-Z template used in this session did not expose `#news-card`.
- The actual screenshot anchor was `#slide`.
- If Playwright stalls waiting for a missing selector, inspect the template DOM before changing the data pipeline.

## Verification pattern
- Run a 1-item dry-run first.
- Confirm the manifest writes the source label, caption, hashtags, and backtest fields.
- Check that the PNG lands in `data/genz-news/<timestamp>/`.
- If the title clips, fix headline shortening before increasing the batch size.

## Secret handling
- Keep Telegram/API keys in env vars only.
- Never echo raw tokens or cookies in manifests, logs, or final replies.
