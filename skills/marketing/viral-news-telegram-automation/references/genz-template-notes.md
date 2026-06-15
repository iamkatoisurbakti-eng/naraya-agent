# Gen-Z News Template Notes

Current template used in this session:
- `/root/template-genz-news.html`

Layout facts:
- Canvas size: 1250x1000
- Top image zone: 600px high
- Bottom content panel: 400px high
- Placeholder title text: `Tulis Judul Berita Anda Di Sini`
- Placeholder summary text: `Tambahkan deskripsi singkat atau sub-judul berita di sini untuk konteks tambahan.`
- Main image element target: `#news-image`
- Card wrapper target: `#news-card`

Rendering notes:
- Inject the generated image as a data URL into `#news-image`.
- Screenshot the `#news-card` element at a small viewport for Telegram-ready PNG output.
- Keep headline fitting conservative: prefer first sentence or first clause, then cap to ~6–8 words.
- Avoid slicing mid-clause; shorten by removing trailing context words.
- Remove source suffixes and noisy prefixes before fitting text.

Delivery notes:
- Send each PNG to Telegram as a document with a short Gen-Z caption.
- Caption structure used in this session:
  - `Hook: ...`
  - `Viral momentum: ...`
  - blank line
  - CTA line
  - blank line
  - hashtags
