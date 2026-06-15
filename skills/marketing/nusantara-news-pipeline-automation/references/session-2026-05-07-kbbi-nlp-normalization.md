# Session note: KBBI NLP normalization gate (2026-05-07)

Context: user requested that all script/naskah inputs be Bahasa Indonesia baku and follow KBBI, using NLP tools to normalize spelling, word breaks, abbreviations, and slang before video/script publication.

Repo implementation pattern:
- Add reusable service: `/root/nusantara-ai-saas/src/services/indonesian-nlp.ts`.
- Unit tests: `/root/nusantara-ai-saas/tests/unit/indonesian-nlp.test.ts`.
- Integrate normalization in these pipeline touchpoints:
  - `scripts/genz-news.ts` for generated title/caption/hashtags/card text.
  - `src/services/news-articles.ts` for public article title/body/slug text.
  - `scripts/youtube-shorts-upload.ts` for YouTube title/description metadata.
  - `scripts/news-pipeline.ts` immediately after loading `manifest.json`, before image/video/article/report distribution.

Core behavior to preserve:
- `normalizeIndonesianFormalText(text)` normalizes a single title/sentence/paragraph.
- `normalizeIndonesianMultilineText(text)` normalizes each caption line while preserving blank lines; use this for Instagram/YouTube captions so formatting is not flattened.
- `normalizeIndonesianScriptPacket(packet)` normalizes handoff fields from Script Writing Agent before Visual & Audio Creation Agent.
- `analyzeIndonesianTextQuality(text)` returns normalized text, removed slang, unresolved slang, and score for QC.

Known replacements worth keeping/expanding:
- `gak/nggak/ga/enggak` -> `tidak`
- `gue/gua` -> `saya`; `lo/lu` -> `kamu`
- `guys` -> `teman`; `netizen` -> `warganet`
- `bgt/banget` -> `sekali`; `rame` -> `ramai`; `bikin` -> `membuat`
- `subscribe` -> `berlangganan`; `share` -> `bagikan`; `update` -> `pembaruan`; `scroll` -> `menggulir layar`
- `gandeng` -> `menggandeng`; `garap` -> `menggarap`
- `no running text` -> `tidak ada teks berjalan` for public-facing script direction.

Verification commands:
```bash
cd /root/nusantara-ai-saas
npm run test:unit -- --runTestsByPath tests/unit/indonesian-nlp.test.ts
npm run build:server
NEWS_LANGUAGE_DICTIONARY_MODE=kbbi NEWS_CONTENT_LANGUAGE_STYLE=baku-indonesia NEWS_VIDEO_USE_REFERENCE_IMAGE=0 NEWS_NATURAL_NARRATION=0 NEWS_TTS_PROVIDER=disabled npm run gen:news-pipeline -- --count 1 --dry-run --skip-youtube --skip-telegram
```

Dry-run validation should inspect `pipeline-report.json` for title/captions and ensure no informal tokens remain. Do not print secrets or `.env` values.

Pitfalls:
- Do not normalize whole multiline captions with a single paragraph normalizer; it removes line breaks. Use `normalizeIndonesianMultilineText`.
- Keep hashtags as hashtags; normalize words inside tags only if the function explicitly preserves `#` formatting.
- KBBI mode should not trigger OpenAI TTS; current audio policy stays generated-video/SEEDANCE ambience only.
- If a term is informal but common in news metadata, add both a replacement rule and a unit test before relying on it in production.
