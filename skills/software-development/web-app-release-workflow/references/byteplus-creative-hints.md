# BytePlus creative hints for news video

Use these only when the story benefits from an on-screen presenter or branded frame.

Environment/CLI knobs
- `NEWS_VIDEO_DIGITAL_CHARACTER`
- `NEWS_VIDEO_TEMPLATE`
- `NEWS_VIDEO_ELEMENT`
- Matching CLI flags in the video generator

Rule of thumb
- Breaking news: usually no digital character; keep the story visual and headline-led.
- Explainer/interview/hosted format: enable digital character when it clarifies the story.
- Graphic-heavy coverage: enable template/element hints only if they improve clarity.

Implementation note
- Keep hints optional and pass them only when set.
- Do not hardcode one always-on template across all news outputs.
- Keep the prompt news-centric; hints should support the story, not replace it.

Verification
- Dry-run should show the selected hints in the emitted payload.
- If no env vars are set, the pipeline must still generate normally.