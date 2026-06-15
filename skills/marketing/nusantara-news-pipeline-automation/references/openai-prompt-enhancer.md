# OpenAI prompt enhancer for flyers

Use GPT-4o as a prompt-rewrite stage for Nusantara-AI News flyers when the user wants cleaner composition before image generation.

## When to use
- The raw news prompt is too literal, too long, or too inconsistent for image generation.
- The user explicitly asks to use GPT-4o for flyer generation assistance.
- You want to keep the image provider unchanged but improve the prompt quality first.

## Recommended env
- `NEWS_FLYER_PROMPT_PROVIDER=openai`
- `NEWS_FLYER_PROMPT_MODEL=gpt-4o`

## Behavior
- Send the raw flyer prompt to OpenAI first.
- Return only a single cleaned-up prompt.
- Do not add bullets, quotes, or explanations in the enhancer output.
- Feed the rewritten prompt into the image-generation provider afterward.

## Pitfalls
- Prompt enhancement is not the same as image generation; a successful rewrite does not mean the image provider is ready.
- OpenAI image calls can fail with org-verification HTTP 403 even if GPT-4o prompt rewriting works.
- Ark/Byteplus image calls can fail on billing/account errors; verify provider readiness before promising fresh renders.
