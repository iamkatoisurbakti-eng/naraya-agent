# Session notes: source registry + KBBI scoring

Date: 2026-05-07

## What changed in practice
- Local repo `api-publik/indonesia` was already available under `/root/.hermes/vendor/indonesia` and is best treated as a read-only registry snapshot source.
- The generator should parse README section headings (for example: berita, hiburan, kesehatan), then write a per-run JSON snapshot into the run directory so the exact source set is reproducible.
- Local repo `KBBI-SQL-database` was cloned under `/root/.hermes/vendor/KBBI-SQL-database` and `dictionary_JSON.json` is usable as a lexical quality signal.
- KBBI coverage should stay a soft signal: it helps language quality, but should not overpower freshness, relevance, or story fit.

## Practical verification
- After source integration, run a 1-item or 10-item dry-run with `--template /root/template-genz-news.html`.
- Check that the manifest records:
  - source order / registry source
  - registry sections loaded
  - kbbi source
  - backtest or overlap metrics if present
- Check that the run directory includes the registry snapshot JSON.

## Useful paths
- `/root/.hermes/vendor/indonesia/README.md`
- `/root/.hermes/vendor/KBBI-SQL-database/dictionary_JSON.json`
- `/root/nusantara-ai-saas/scripts/genz-news.ts`
- `/root/template-genz-news.html`
