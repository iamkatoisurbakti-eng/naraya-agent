# Filter Agent keyword database and text preprocessing session notes

Context: Nusantara-AI Filter Agent was upgraded from static JSON keyword lists to a SQLite-backed negative keyword database plus text preprocessing before matching.

## Stable repo artifacts

- Config: `/root/nusantara-ai-saas/config/content-filter.json`
- Runner: `/root/nusantara-ai-saas/scripts/content-filter.mjs`
- SQLite DB: `/root/nusantara-ai-saas/data/content-filter/negative-keywords.db`
- Reusable TS preprocessor: `/root/nusantara-ai-saas/src/services/text-preprocess.ts`

## Database schema

`filter_keywords` stores:
- `category`
- `term`
- `term_hash`
- `severity`
- `action` (`BLOCK` or `REVIEW`)
- `enabled`
- `locale`
- `source`
- timestamps

`filter_audit` stores only non-secret/safe audit info:
- `decision`, `severity`, `categories`, `matched_count`
- `matched_term_hashes`
- `checked_fields`
- `content_hash`

Do not store or print raw sensitive terms in public output.

## Default env

```env
NEWS_FILTER_ENABLED=1
NEWS_FILTER_CONFIG_PATH=/root/nusantara-ai-saas/config/content-filter.json
NEWS_FILTER_USE_KEYWORD_DB=1
NEWS_FILTER_KEYWORD_DB_PATH=/root/nusantara-ai-saas/data/content-filter/negative-keywords.db
NEWS_FILTER_BLOCK_CATEGORIES=pornography,pedophilia,violence,religion,politics
NEWS_FILTER_FAIL_CLOSED=1
NEWS_TEXT_PREPROCESS_ENABLED=1
NEWS_TEXT_PREPROCESS_LOWERCASE=1
NEWS_TEXT_PREPROCESS_STRIP_HTML=1
NEWS_TEXT_PREPROCESS_UNICODE=1
NEWS_TEXT_PREPROCESS_WHITESPACE=1
NEWS_TEXT_PREPROCESS_LEETSPEAK=1
NEWS_TEXT_PREPROCESS_ZERO_WIDTH=1
NEWS_TEXT_PREPROCESS_REPEAT_CHARS=1
```

## Commands

Run from `/root/nusantara-ai-saas`:

```bash
node scripts/content-filter.mjs --init-db
node scripts/content-filter.mjs --stats
node scripts/content-filter.mjs --preprocess-only --text='teks untuk dicek'
node scripts/content-filter.mjs --text='teks untuk dicek'
```

Exit codes:
- `0` PASS
- `1` REVIEW
- `2` BLOCK or fail-closed

## Text preprocessing behavior

Before keyword matching, normalize:
- Unicode NFKC, smart quotes/dashes
- HTML tags/entities
- zero-width characters
- lowercase
- whitespace
- light leetspeak (`4`→`a`, `3`→`e`, `1`→`i`, `0`→`o`, `5`→`s`, `7`→`t`)
- repeated letters
- URLs and noisy separators

The filter output should expose only preprocessing metadata:
- `preprocessing.enabled`
- `preprocessing.changed`
- `preprocessing.transformations`
- `preprocessing.normalized_hash`

Do not include the full normalized text in routine/public filter output.

## Validation pattern

```bash
set +e
node scripts/content-filter.mjs --text='Kabar positif tentang inovasi pendidikan Indonesia'; echo pass=$?
node scripts/content-filter.mjs --text='<b>kampanye</b> p4rtai p0litik menjelang pemilu'; echo block=$?
node scripts/content-filter.mjs --text='Pemerintah menyiapkan regulasi baru untuk transportasi publik'; echo review=$?
npm run build:server
```

Expected:
- safe text: `PASS`, exit `0`
- forbidden/obfuscated text: `BLOCK`, exit `2`
- context review term: `REVIEW`, exit `1`
- `keyword_source: database`
- no raw matched terms in JSON output
