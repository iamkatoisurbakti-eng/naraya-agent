# Seedream 4.0 image batch note

Session note for Nusantara-AI News image generation.

## Default model
- Use the Ark/BytePlus images endpoint for Seedream 4.0 requests.
- Preferred model: `seedream-4-0-250828`
- Endpoint: `https://ark.ap-southeast.bytepluses.com/api/v3/images/generations`

## Payload shape used in this stack
- `model`: `seedream-4-0-250828`
- `prompt`: cleaned prompt from the flyer prompt stage
- `sequential_image_generation`: `disabled`
- `response_format`: `url`
- `size`: usually `2K`
- `stream`: `false`
- `watermark`: set from env/default policy; keep disabled unless explicitly requested

## Batch-limit convention
- If the user says `limit 200pcs`, interpret that as a per-run batch cap of 200 generated images.
- For jobs larger than 200, split into multiple batches/runs instead of forcing one oversized request.
- Verify the resulting manifest/count before reporting success.

## Pitfalls
- Do not hardcode secrets in the prompt or command examples.
- If a live API token is pasted in chat, treat it as exposed and tell the user to rotate it.
- A prompt rewrite success does not mean image generation succeeded; confirm the provider response or manifest output.
