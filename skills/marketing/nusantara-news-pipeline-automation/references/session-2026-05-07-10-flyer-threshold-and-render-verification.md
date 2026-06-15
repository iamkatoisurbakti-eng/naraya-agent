# Session note: 10-flyer pack threshold and render verification

## What happened
- Running `npm run gen:viral-news -- --count 10 --dry-run` with the default score gate produced only 8 items.
- Re-running with `NEWS_MIN_SCORE=90 NEWS_MIN_SINGLE_SCORE=90 npm run gen:viral-news -- --count 10 --dry-run` produced 10 rendered PNGs.
- Rendered PNGs were created under `data/genz-news/<timestamp>/` and each file was verified as `2160 x 2700` via `file`.

## Lesson
- Exact-count flyer packs can require a lower score threshold than the default strict gate.
- For requested 10-item Instagram packs, lower the threshold first, then verify the final count and PNG dimensions before claiming success.
- If the count is still short, do not silently pad with low-quality items; report the shortfall or rerun with adjusted gates.
