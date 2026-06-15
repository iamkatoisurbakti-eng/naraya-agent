# Session note: 4:5 template positioning + natural narration

Date: 2026-05-07

## What changed
- The 4:5 Instagram template was tightened by reducing the empty top band and moving the hero image upward.
- The image slot now works better with `object-position: center center` and a tiny scale-up (`transform: scale(1.01)`) so the subject feels more centered.
- Natural narration was tuned toward a male Indonesian news-presenter voice.

## Practical rules
- Prefer a shorter top empty band for 4:5 news cards when the hero image looks too low.
- Center the hero crop unless the source image has a strong subject near the top edge.
- Avoid overly chatty narration intros; use a clean news-anchor opening.
- When building narration from a manifest, drop or ignore summaries that already contain ellipses/truncation markers (`...` or `…`) so the TTS script does not repeat broken fragments.
- Keep the TTS character description explicit: male presenter, natural, warm, firm, clear articulation, neutral Indonesian, credible broadcast feel.

## Verification
- Use `ffprobe` to confirm the final video remains 9:16 with audio.
- Check the rendered 4:5 card visually for balanced negative space above the hero image.
