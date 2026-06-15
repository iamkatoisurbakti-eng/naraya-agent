# KSR888 banner folder + slider fallback

Session note: KSR888 banner visuals were stabilized by treating `/root/nusantara-ai-saas/KSR888/banner/` as a first-class asset source, copied into the PHP image at `/var/www/html/banner/`.

Important scope note: this is the legacy desktop/mobile slider fallback. The main Laravel homepage (`/`, `resources/views/welcome.blade.php`) is DB-backed and renders `asset('storage/' . $banner->gambar)`. For normal homepage banner additions, follow `references/ksr888-homepage-banner-ingestion.md`: copy assets to `site/public/storage/post-images`, add active rows to `banner`, and verify homepage HTML references `/storage/post-images/...`.

What changed
- Desktop/mobile slider templates now build a banner list from `tb_banner` first.
- They then append any image files found in the local `banner/` folder as fallback/extra slides.
- Each banner uses a full public URL under `/banner/<filename>` so the live host can serve it directly.

Deploy detail
- `KSR888/docker/php/Dockerfile` must include:
  - `COPY KSR888/banner/ /var/www/html/banner/`
- Rebuild/recreate `ksr888-web` after any banner source changes.

Verification pattern
- Fetch the live pages with a browser-like User-Agent.
- Confirm `https://ksr888.online/dekstop/index.php` and `https://ksr888.online/mobile/index.php` return `200`.
- Extract banner image URLs from the rendered HTML and `HEAD`/GET each one.
- Expected result from this session: 8 banner URLs on each page, `bad 0`.

Pitfall
- Browser automation may still fail in this environment with Chromium `ProcessSingleton` / `Failed to create socket directory` errors. When that happens, fall back to direct HTTP and bundle/HTML verification instead of retrying the same browser launch.