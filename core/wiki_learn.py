import time
import json
from pathlib import Path
import wikipediaapi

OUT = Path("data/wiki_raw")
OUT.mkdir(parents=True, exist_ok=True)

wiki = wikipediaapi.Wikipedia(
    user_agent="NarayaAgent/1.0 (learning; contact: admin@nusantra.local)",
    language="id"
)

TOPICS = [
    "Sejarah Indonesia",
    "Hindia Belanda",
    "Kebangkitan Nasional Indonesia",
    "Sumpah Pemuda",
    "Proklamasi Kemerdekaan Indonesia",
    "Revolusi Nasional Indonesia",
    "Orde Lama",
    "Orde Baru",
    "Reformasi Indonesia",
    "Sejarah dunia",
    "Perang Dunia I",
    "Perang Dunia II",
    "Perang Dingin",
    "Globalisasi",
    "Internet",
    "Kecerdasan buatan"
]

def save_page(title):
    page = wiki.page(title)

    if not page.exists():
        print("MISS:", title)
        return

    data = {
        "title": page.title,
        "summary": page.summary,
        "text": page.text,
        "url": page.fullurl,
        "source": "wikipedia_id"
    }

    path = OUT / f"{title.replace('/', '-')}.json"
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("SAVED:", title)

def main():
    for topic in TOPICS:
        save_page(topic)
        time.sleep(1)

if __name__ == "__main__":
    main()
