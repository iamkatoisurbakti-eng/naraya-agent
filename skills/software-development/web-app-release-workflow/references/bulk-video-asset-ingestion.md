# Bulk Video Asset Ingestion for Landing Pages

Use this when the user wants to add all videos from a folder into the website so the landing/showreel looks fuller.

## Pattern used in this repo
- Source folder can live outside `web/public/` (for example `/root/nusantara-ai-saas/video`).
- Copy every media file into a Vite-served public directory such as `web/public/video-website/`.
- Reference assets with root-relative URLs like `/video-website/<filename>.mp4`.
- Build a data array from the actual file list rather than hand-picking one showcase clip.
- When there are many clips, switch from a single preview to a grid/card showreel with per-item metadata.
- If filenames are ugly, use neutral titles like `Reel 01`, `Reel 02` instead of raw filenames.

## Practical steps
1. Inspect the source folder contents with the terminal and count the files.
2. Copy the files into `web/public/<slug>/` so Vite serves them.
3. Update the React source array to include every copied video.
4. If the UI currently assumes a single preview, switch it to a grid or slider with per-item metadata.
5. Rebuild the web app and deploy.
6. Verify live DOM/media counts in a browser session, not just the build output.

## Pitfalls
- Do not edit `web/dist/`; it is a build artifact.
- Do not leave the JSX array pointing at only one example file after the bulk copy.
- If there are duplicate media paths in `web/public/` and another folder, make the landing page point to the intended canonical folder.
- Large grids can feel cramped on mobile; verify a desktop and mobile viewport.
- After deploy, verify that the live page actually renders the expected number of `<video>` elements.
