# News source registry and delivery notes

Session takeaway for the viral news pack workflow:

- Preferred source order in `scripts/genz-news.ts` is now:
  1. Berita Indo API / multi-source Indonesian news
  2. `DAFTAR_API_LOKAL_INDONESIA_URL` registry-backed endpoints
  3. legacy fallback feeds
- The generator was verified with `--template /root/template-genz-news.html` for the Gen-Z layout.
- Dry-run generation is useful for verifying the manifest, ranks, and rendered PNGs before any Telegram send.
- For video-pack variants, the ARK/BytePlus request config may be loaded from `/root/api-video.txt`; treat it as secret material and never echo the values.
- If a single media item fails during a batch, retry only that item instead of rerunning the full pack.
- Telegram delivery should be verified per item when possible; keep the final send step separate from render/generation verification.
