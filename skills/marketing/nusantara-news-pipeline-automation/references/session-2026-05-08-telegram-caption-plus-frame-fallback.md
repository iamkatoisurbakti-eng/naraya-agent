# Telegram caption + frame fallback notes

Session note for end-to-end news delivery runs.

## What worked
- Sending the rendered flyer PNG with the Telegram send tool using a `MEDIA:/absolute/path/to/file.png` line in the message body.
- Including a complete caption block directly in the same Telegram message.
- Appending exactly 4 hashtags in the caption block.
- Sending short assets as individual frame PNGs when the full video stage was blocked.

## Delivery shape
- Flyer item:
  - caption + 4 hashtags
  - one PNG path
- Short item:
  - send each frame one-by-one when no valid MP4 is available
  - label frames plainly (`Short frame 1`, `Short frame 2`, etc.)

## Verification
- Confirm the PNG exists before sending.
- Confirm the frame PNGs exist before sending them individually.
- If a provider/model error blocks video generation, do not stop the distribution run; fall back to the verified frame PNGs already on disk and report that the delivery used fallback frames.