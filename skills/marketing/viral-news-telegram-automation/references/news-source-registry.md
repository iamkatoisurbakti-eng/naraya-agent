# News source registry notes

Session note for GEN-Z news automation.

## Registry pages
- Daftar API Lokal Indonesia: https://farizdotid.github.io/DAFTAR-API-LOKAL-INDONESIA/#/
- Raw README (easier to parse in automation work): https://raw.githubusercontent.com/farizdotid/DAFTAR-API-LOKAL-INDONESIA/master/README.md

## News section entries
The registry’s news section includes:
- API Berita Indonesia (R.M. Reza)
- Berita Indo API (Satya Wikananda)
- CNN Indonesia
- Detik News API
- Indonesia news API
- Jakarta Post API
- The Lazy Media API

## Practical automation notes
- Treat the registry as a discovery source, not a guaranteed live API endpoint.
- In this session, the `api-berita-indonesia.vercel.app` demo endpoint responded with `DEPLOYMENT_DISABLED` / payment-required text, so it should remain a best-effort fallback only.
- Prefer direct working feeds already verified by the generator, and keep the registry as a source list for expanding coverage.
- If a project uses an env override, prefer a dedicated URL like `DAFTAR_API_LOKAL_INDONESIA_URL` rather than hardcoding the registry page.
