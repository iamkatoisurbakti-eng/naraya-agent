# KSR888 Mobile GAME TERPOPULAR Local Art Assets

Use this when the mobile `GAME TERPOPULAR` strip should render with local artwork instead of remote game thumbnails.

## Asset source
- Source folder provided by the user: `/root/nusantara-ai-saas/KSR888/GAME POPULER`
- Files available in this session:
  - `game-image-proxy.webp`
  - `game-image-proxy (1).webp` through `game-image-proxy (10).webp`

## Deployment pattern
- Copy the source images into the Laravel public web root before verification.
- Prefer normalized filenames without spaces for live assets, e.g.:
  - `public/assets/img/game-populer/game-populer-01.webp`
  - `public/assets/img/game-populer/game-populer-02.webp`
  - ...
  - `public/assets/img/game-populer/game-populer-11.webp`
- Render those public paths from the mobile Blade template.

## Verification
- Confirm the mobile HTML contains `GAME TERPOPULAR` and the normalized filenames.
- Confirm live asset requests return HTTP 200 for the public paths.
- Test with a mobile user-agent; do not trust the desktop branch alone.

## Pitfalls
- Filenames with spaces can be awkward in HTML/CURL verification and are easy to mis-handle in deployment.
- A mobile carousel can look fine in source but still show stale remote images if the public asset copy was skipped.
- If the page uses `@desktop` / `@elsedesktop`, update both branches or shared helpers so they stay visually aligned.
