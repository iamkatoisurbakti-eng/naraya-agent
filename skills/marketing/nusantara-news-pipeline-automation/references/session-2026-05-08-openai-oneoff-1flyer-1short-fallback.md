# OpenAI one-off fallback: 1 flyer + 1 short

Session finding:
- When the Ark video model `seedance-1.5-pro` was unavailable (`InvalidEndpointOrModel.NotFound`), a one-off fallback package could still produce a valid deliverable using OpenAI for images + Sora for video.
- The fallback package produced:
  - 1 flyer PNG via OpenAI image generation, rendered through `templates/nusantara_instagram_4x5.html`
  - 1 short video built as 5 scenes × 4 seconds = ~20 seconds total
  - browser-rendered transparent title overlay for Shorts
  - Telegram delivery after both assets existed

Working notes:
1. Use a wrapper script or job that generates the flyer first, then 5 separate Sora scenes, then concatenates to a raw 20s vertical short.
2. Keep the shorts title overlay browser-based if ffmpeg text rendering shows boxed/garbled glyphs.
3. For Playwright on this host, Chromium was available at `/snap/bin/chromium`; launch with `--no-sandbox --disable-setuid-sandbox` when needed.
4. Verify the final short with `ffprobe` and a sampled frame before sending.

Pitfalls:
- OpenAI image generation can return a transient 500 server error; retry the request or rerun the fallback package rather than treating it as a permanent failure.
- Do not reuse the fallback as the primary pipeline if the Ark/Seedance route is healthy; it is an emergency path for delivery continuity.
