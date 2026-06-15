# Session note: GPT-4o flyer prompt enhancer + provider gates

What changed in this session:
- Added a GPT-4o prompt-rewrite stage for flyer generation.
- Pipeline can now send the raw flyer prompt through OpenAI first, then pass the cleaned prompt to the image provider.

Observed provider behavior:
- OpenAI `gpt-image-2` calls can fail with HTTP 403 when the organization is not verified.
- Ark/Byteplus image or video tasks can fail with `AccountOverdueError` when the account balance is overdue.

Operational lesson:
- Treat prompt enhancement and image generation as separate stages.
- A successful GPT-4o rewrite does not imply the final image provider is ready.
- For fresh renders, verify provider readiness before promising output; otherwise reuse verified assets from `data/genz-news/**` or run dry-run / prompt-only flows.
