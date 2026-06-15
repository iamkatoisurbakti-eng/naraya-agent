# Seedream / BytePlus ARK image pipeline notes

Session pattern:
- Use BytePlus ARK image generation endpoint:
  `POST https://ark.ap-southeast.bytepluses.com/api/v3/images/generations`
- Known working image model in this session: `seedream-5-0-260128`
- Useful request fields:
  - `response_format: "url"`
  - `size: "2K"`
  - `stream: false`
  - `watermark: false` to remove the AI watermark
  - `sequential_image_generation: "disabled"` when a single image is enough
- The API can return a signed JPEG URL; download it locally before delivery.

Practical workflow:
1. Generate with `watermark: false` when the user explicitly wants a clean asset.
2. Download the returned URL with `curl -L -sS` to a local `.jpeg`.
3. Convert to `.png` with a deterministic CLI tool available in the environment (for example `ffmpeg -i input.jpeg output.png`).
4. Verify the output visually before delivery when the user is sensitive to render quality.
5. Send to Telegram with the requested caption once the bot token and chat ID are available.

Telegram notes:
- If the user wants the exact PNG preserved, `sendDocument` is the safest delivery mode.
- If the user wants chat-inline preview, `sendPhoto` is usually better.
- If the token or chat ID is missing from env/config, ask for them rather than guessing.
- Do not keep or repeat live token values in the skill text.

Pitfalls:
- Some image APIs return a JPEG even when the user expects PNG; convert locally if you need PNG.
- Watermark removal is controlled by request parameters, not by post-processing alone.
- Verify that the downloaded file size is non-zero before conversion or upload.
- A rendered image can be visually fine even when its dimensions differ from the intended social format; check both.
