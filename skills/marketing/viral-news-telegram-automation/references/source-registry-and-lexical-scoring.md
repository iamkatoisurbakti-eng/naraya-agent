# Source registry + lexical scoring notes

This workflow learned two useful integrations:

1. Local Indonesian API registry snapshots
   - Mirror the upstream README into `/root/.hermes/vendor/<repo>/README.md`.
   - Extract section-specific URLs by heading, not by hardcoded source list.
   - For api-publik/indonesia, the useful sections in this session were:
     - `### Berita`
     - `### Hiburan`
     - `### Kesehatan`
   - Save a per-run snapshot JSON in the output directory so later debugging can see exactly what registry sections were loaded.

2. KBBI lexical quality scoring
   - Use a local dictionary dump such as `/root/.hermes/vendor/KBBI-SQL-database/dictionary_JSON.json`.
   - Build a cached word set from `dictionary.dictionary[].word`.
   - Score title/summary coverage by checking how many tokens exist in the dictionary.
   - Use the score as a light quality signal, not a hard filter, so news selection still favors relevance and freshness.

Pitfalls:
- Do not assume a registry README is machine-friendly; parse headings and URLs defensively.
- Keep the KBBI signal lightweight so it improves Indonesian naturalness without hiding good proper nouns or brand names.
- If a repo/vendor path is missing, fall back gracefully and keep the run working.
