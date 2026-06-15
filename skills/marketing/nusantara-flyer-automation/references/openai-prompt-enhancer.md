# OpenAI prompt enhancement for flyer generation

Use this when you want GPT-4o to refine a flyer prompt before the image model runs.

## Env
- `NEWS_FLYER_PROMPT_PROVIDER=openai`
- `NEWS_FLYER_PROMPT_MODEL=gpt-4o`

## Behavior
- `scripts/prompt-to-images.ts` first rewrites the raw prompt with OpenAI chat completions.
- The returned text becomes the final prompt sent to the image provider.
- If the prompt enhancer is disabled or the OpenAI key is missing, the raw prompt is used unchanged.

## Good use cases
- Make a raw flyer idea more editorial, concise, and image-model friendly.
- Add structure: headline concept, full-frame composition, clean negative space, realistic news photo look.
- Keep the final prompt single-paragraph and direct.

## Pitfalls
- This does **not** fix an unavailable image provider.
- If OpenAI image generation is blocked by org verification or Ark is over quota, prompt enhancement may still succeed while final rendering fails.
- Do not send a prompt that already contains long safety boilerplate if you want the enhancer to produce compact output; keep the seed prompt short and specific.

## Verification
- Run with `--dry-run` to confirm the enhancer is active without spending image credits.
- The dry-run JSON should show the final prompt payload after enhancement.
