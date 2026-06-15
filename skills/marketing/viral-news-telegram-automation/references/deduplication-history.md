# Deduplication for GEN-Z News Automation

Use `data/genz-news/history.json` as the long-term memory of already-published stories.

## Current rule set
Reject a candidate if any of these match a prior item:
- canonical key match: normalized `title + url`
- normalized title match
- compact title match: remove punctuation/extra whitespace/lowercase
- text overlap with history at or above the tuned threshold (`>= 0.35`)

## Storage rule
When saving a successful story, persist:
- `key`
- `title`
- `summary`
- `source`
- `publishedAt`

## Operational note
If the user asks for “jangan ada duplikat berita”, apply this filter before ranking so duplicate stories do not consume a slot in the final batch.
