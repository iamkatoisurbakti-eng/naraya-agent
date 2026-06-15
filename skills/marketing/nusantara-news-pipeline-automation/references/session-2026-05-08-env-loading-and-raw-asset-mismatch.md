# Session 2026-05-08: env loading and raw-asset mismatch

## What happened
- Sourcing `/root/nusantara-ai-saas/.env` directly in a shell exposed unquoted multi-word values as commands (for example `TELEGRAM_FIRST_NAME=Nusantara Ai` and similar fields with spaces).
- The fix was to quote any `.env` values containing spaces before shell sourcing.
- In the same run, the pipeline had a rendered Instagram PNG in `data/genz-news/<timestamp>/`, but `gen:news-youtube-upload` failed because `generateInstagramAssets` looked for the raw image at `instagram-4x5-raw/<slug>-raw.png` and did not find it.

## Practical rule
- Treat shell-sourced `.env` files as stricter than dotenv parsing: quote every value with spaces before running `source .env` or `. ./.env`.
- When a pipeline run has a final template PNG but no raw provider asset, inspect the run directory and manifest before retrying. Do not assume the presence of the rendered PNG is enough for downstream image/video steps.
