# Heatmap Clipper integration and homepage reel removal notes

Session takeaways for this repo:

- Homepage media arrays live in `web/src/components/LandingPage.tsx`; removing one reel means deleting the source entry, rebuilding, and checking the built bundle for the stale visible string.
- The live homepage may block non-browser tooling with 403, so verify with `curl -A 'Mozilla/5.0' -L` when scraping public pages.
- Heatmap Clipper was integrated as an auth-protected backend route plus worker script:
  - backend route: `/api/heatmap-clipper`
  - worker: `scripts/heatmap-clipper-worker.py`
  - UI: dashboard panel
- For route tests that mock `spawn`, return an `EventEmitter` child with `stdout`/`stderr`, and emit stdout data + `close` asynchronously (`setImmediate`) so request handlers can attach listeners before the payload is sent.
- When worker/job state is persisted as JSON text, prefer a defensive parser like `parseJsonArray()` for `stages_json`, `outputs_json`, and selected segment fields.
- After deploy, verify both:
  - `/api/health` returns 200
  - the integrated route returns 401/403 without auth, proving it is mounted and protected
