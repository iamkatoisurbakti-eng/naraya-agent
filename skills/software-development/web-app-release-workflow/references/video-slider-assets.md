# Landing-page video slider notes

Observed asset layout:
- Source/public assets should live under `web/public/video-website/`.
- The slider can reference files with root-relative URLs like `/video-website/<file>.mp4`.

Files used in this repo session:
- `eac5838f-a9f2-4295-b494-dc18831f71c7_hd.mp4`
- `c62aab0e-2749-45ba-abf3-f8bb827592bc_hd.mp4`
- `b4384ae8-717c-4f29-93ee-e300cb7504d1.mp4`
- `819d5cf3-9ace-476a-a1ce-062d7051288f_hd.mp4`
- `253a6a4c-d8d0-4d9e-8cc1-f99675021cf1_hd.mp4`
- `0136bf9d-a9ec-49c8-896d-41ebdc98860d.mp4`

Implementation notes:
- Use a `useState` index for the current video.
- Advance with a timer inside `useEffect` and clear it on cleanup.
- Use `key={currentVideo}` on the `<video>` element if you want a clean remount on switch.
- Keep overlays inside a `relative` wrapper when using absolute-positioned captions/buttons.
- `autoPlay muted loop playsInline preload="metadata"` is the safest baseline for decorative hero videos.
