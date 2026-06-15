# Mobile browser UX notes

Used in the mobile usability pass for Nusantara AI.

Key patterns that worked well:
- Prefer mobile-first source edits in `web/src/components/*` and `web/src/styles/index.css`.
- Keep the top nav compact on small screens:
  - stack logo + actions vertically when needed
  - use a short horizontal chip row with `overflow-x-auto`
  - shorten long CTA labels on mobile if they wrap or clip
- Make primary CTA buttons full-width or stacked on phones; avoid dense two-column button rows.
- Reduce large hero media on phones when it hurts readability or performance; hiding background video on mobile can improve clarity.
- Keep news/article cards single-column on mobile with smaller image heights and readable title sizes.
- Add `overflow-x: hidden`, `touch-action: manipulation`, and a small `scroll-padding-top` for anchored sections.

Verification pattern:
1. Build web: `npm run build:web`
2. Deploy: `bash scripts/deploy.sh`
3. Capture mobile screenshots with Chromium headless at `390x844`
4. Inspect screenshots for:
   - clipped headings or buttons
   - crowded chips/tabs
   - awkward horizontal overflow
   - touch targets that are too small
5. If needed, iterate on the source components and re-run the same checks.
