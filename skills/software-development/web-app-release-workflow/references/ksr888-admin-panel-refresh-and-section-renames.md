# KSR888 admin panel refresh and section rename notes

Use this note for KSR888-style imported PHP admin panels where the user wants behavior fixes without changing appearance.

## Banner CRUD refresh
- For `/banner`, make `store`, `update`, and `destroy` return `redirect()->route('banner.index')` (or the equivalent index route) so the page refreshes on the banner listing itself.
- Do **not** redirect to home after editing a banner; the expected UX is to stay on the banner page and show the updated list/flashdata immediately.
- Keep the success flash message simple (`Data berhasil diubah`, `Data berhasil dihapus`).

## Setting website section names
- Rename tab labels in place; do not redesign the form.
- Keep `id` / `href` / `aria-controls` / `aria-labelledby` pairs synchronized when renaming tabs.
- The common section order used in this session was:
  1. Info Website
  2. Contact
  3. Appearance
  4. AutoGoPay QRIS
  5. Setting Slider Banner
  6. Setting Pop Up
  7. Setting DP-WD
  8. Setting API
  9. Notifikasi

## Data Member column order
- When the user asks for a new table layout, patch the Blade header and the DataTables `columns` array together.
- Keep visible order aligned with the requested columns; in this session the target was:
  `NO | Username | Email | Rekening | No Hp | Refferal | Tanggal Daftar`
- If a hidden action column is no longer wanted, remove it from both the header and the JS config instead of hiding it only with CSS.

## Verification
- After patching, run a syntax check in the live PHP container if host PHP CLI is unavailable locally.
- Deploy and verify the public/admin page with HTTP when browser automation fails.
- Use cache-busting only when a stale asset is the problem; for pure CRUD/section rename fixes, the main check is whether the route now returns the refreshed page with the updated content.