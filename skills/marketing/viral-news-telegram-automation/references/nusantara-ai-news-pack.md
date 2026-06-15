# Nusantara-AI News pack rules

Session-derived conventions for the news automation pipeline.

## House rules
- Public brand is always `NUSANTARA-AI NEWS`.
- Public copy uses Jaksel/Gen-Z vibe but remains KBBI-friendly.
- Never display source labels or source names in visible output.
- Every generated story should produce two deliverables:
  1. a short video asset
  2. a 5:4 Instagram image asset
- Every video must clearly contain the news title / news hook in the rendered frame.
- Caption copy should always include a viral hook and viral hashtags, including `#HookViral`.
- Final pipeline order: generate news -> render 5:4 image -> render short video -> upload YouTube Short -> send Telegram -> write article -> emit completion report.

## Report expectations
- Include per-item paths for image and video outputs.
- Mark skipped stages explicitly in dry-run mode.
- Emit a final report only after all enabled stages finish.

## Verification
- Run a dry-run first when changing layout or delivery stages.
- Verify the sample asset after branding changes.
- Confirm visible output does not leak source names or internal labels.
