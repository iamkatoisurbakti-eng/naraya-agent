---
name: cnnindonesia-news-api
description: Use when you need to fetch, search, or inspect CNN Indonesia news headlines, categories, and article details from the unofficial Flask API. Provides the endpoints, response shapes, and safe usage patterns.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [news, cnnindonesia, api, scraping, research]
    related_skills: [blogwatcher]
---

# CNN Indonesia News API

## Overview

This skill covers the unofficial CNN Indonesia news API published by the repository `rizki4106/cnnindonesia-news-api`. It exposes a simple Flask service that returns lists of articles for the homepage, category pages, article detail pages, and search results.

Use it when you need Indonesian news items quickly in a structured JSON shape without building your own scraper from scratch.

## When to Use

- You need recent CNN Indonesia headlines for a news bot, dashboard, or content pipeline.
- You need article metadata such as title, image, link, category, or published time.
- You need the full article body from a CNN Indonesia URL.
- You want to search CNN Indonesia by keyword.

Do not use it for:
- Authenticated CNN content or private endpoints.
- Guaranteed-stable production integrations without monitoring, because this is an unofficial scraper.
- Rewriting, republishing, or bypassing source attribution rules.

## API Surface

Base app routes from `main.py`:

- `GET /` → all/news home feed
- `GET /nasional`
- `GET /internasional`
- `GET /ekonomi`
- `GET /olahraga`
- `GET /teknologi`
- `GET /hiburan`
- `GET /gaya-hidup`
- `GET /detail/?url=<cnn-article-url>`
- `GET /search/?q=<keyword>`

## Response Shape

Most endpoints return:

```json
{
  "status": 200,
  "length": 40,
  "data": [
    {
      "judul": "Example title",
      "link": "https://www.cnnindonesia.com/...",
      "poster": "https://...jpg",
      "tipe": "Nasional",
      "waktu": "12 menit yang lalu"
    }
  ]
}
```

Detail endpoint returns:

```json
{
  "status": 200,
  "length": 1,
  "data": [
    {
      "judul": "Article title",
      "poster": "https://...jpg",
      "body": "Full article text..."
    }
  ]
}
```

## Quick Start

### 1) Run the local Flask API

```bash
pip install -r requirements.txt
export FLASK_APP=main.py
flask run
```

### 2) Fetch a category feed

```bash
curl http://localhost:5000/nasional
```

### 3) Search by keyword

```bash
curl 'http://localhost:5000/search/?q=indonesia'
```

### 4) Fetch article details

```bash
curl 'http://localhost:5000/detail/?url=https://www.cnnindonesia.com/internasional/...'
```

## Practical Workflow

1. Pick the category endpoint or search endpoint.
2. Parse `data[]` for titles and image URLs.
3. If you need article text, call the detail endpoint with the article link.
4. Keep output short and normalize title text if using it in a caption or poster.

## Example: Build a News Selection List

```python
import requests

items = requests.get('http://localhost:5000/nasional').json()['data']
for item in items[:5]:
    print(item['judul'], item['link'], item['poster'])
```

## Common Pitfalls

1. **Forgetting this is unofficial.** HTML structure changes on CNN Indonesia can break the scraper.
2. **Assuming every item has full fields.** Some entries can be skipped by the parser if HTML is incomplete.
3. **Using the wrong route spelling.** The live code uses `/gaya-hidup`, not `/gaya-hidupp`.
4. **Expecting search to be perfect.** Results depend on CNN Indonesia’s own site search behavior.
5. **Treating `poster` as permanent.** Image URLs can expire or change.

## Verification Checklist

- [ ] Flask service starts successfully with `python main.py` or `flask run`
- [ ] `GET /` returns JSON with `status`, `length`, and `data`
- [ ] Category endpoints return article lists
- [ ] `GET /detail/?url=...` returns `body` text
- [ ] `GET /search/?q=...` returns matching stories
- [ ] Route names match the current repository code
