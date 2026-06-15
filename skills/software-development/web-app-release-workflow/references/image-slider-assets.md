# Landing-page image preview notes

Observed asset layout:
- Source/generated stills live under `web/public/images-website/`.
- Reference them with root-relative URLs like `/images-website/<file>.jpg`.

Files generated in this repo session:
- `eac5838f-a9f2-4295-b494-dc18831f71c7_hd.jpg`
- `c62aab0e-2749-45ba-abf3-f8bb827592bc_hd.jpg`
- `b4384ae8-717c-4f29-93ee-e300cb7504d1.jpg`
- `819d5cf3-9ace-476a-a1ce-062d7051288f_hd.jpg`
- `253a6a4c-d8d0-4d9e-8cc1-f99675021cf1_hd.jpg`
- `0136bf9d-a9ec-49c8-896d-41ebdc98860d.jpg`

How they were produced here:
- `ffmpeg -y -ss 1.5 -i <source.mp4> -frames:v 1 -vf "scale=960:-1" <output.jpg>`
- Store them in a dedicated public folder instead of `web/dist/` so Vite serves them correctly.

Implementation notes:
- Use a separate state index if the landing page shows both image and video previews.
- If the image preview is decorative, keep the same overlay/caption pattern as the video card for visual consistency.
- If using autoplay for a paired video preview, keep the image slider independent so image switching does not restart video playback.
