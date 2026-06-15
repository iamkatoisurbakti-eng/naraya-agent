# Telegram delivery retry notes

When sending a batch of generated PNG flyers to Telegram:

- Send each PNG with its caption as a single media message.
- If a send fails with flood control / rate limit:
  - wait the suggested cooldown before retrying
  - resend only the failed file, not the entire batch
- If most of the batch already succeeded, keep the successful sends as-is and only recover the failed item.
- Keep captions compact; long captions can make manual resend/debugging harder.
- Do not retry in a tight loop.
