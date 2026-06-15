# Flyer Caption Pack Workflow

Session note: when the user asks for a flyer pack in the form "1 file flyer berikut caption dan 4 hashtag" and wants it split into 10 files, produce one Markdown file per flyer in a dedicated folder.

Recommended file contents per item:
- flyer image path
- caption text
- CTA URL (use the exact URL the user provides if present)
- exactly 4 hashtags

Operational notes:
- Keep filenames canonical and unique per item, using only one numbering scheme.
- After writing the pack, verify the folder contains exactly 10 `.md` files.
- Remove stale duplicates from previous attempts before finalizing.
- The CTA may be a plain URL rather than branded text when the user specifies it.
