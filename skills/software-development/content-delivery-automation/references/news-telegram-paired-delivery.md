# Nusantara-AI news Telegram paired delivery

Use this pattern when a news pipeline must deliver both visual outputs on every run.

## Rule
- For each published news item, send a complete image+video pair to Telegram.
- Send the image first with `sendDocument` so the PNG stays exact.
- Send the final video second with `sendVideo`.
- Only skip an item if either the image file or the video file is missing.

## Caption handling
- Reuse the same story caption for both sends unless the product asks for separate copy.
- Keep captions short enough for Telegram limits.
- Do not restate source labels in the public caption if the brand is meant to stay source-free.

## Delivery hygiene
- Send items sequentially with a small delay between messages to avoid throttling.
- Verify the file exists before reading or uploading it.
- Treat Telegram tokens/chat IDs as secrets; keep them in env only.

## Verification
- Check that the run report marks both image and video as sent for the same item.
- Confirm that Telegram receives two messages per item when both files exist.