# BytePlus/ARK Byte1-Byte14 Automation Index

This reference registers the user-provided `/root/.hermes/Byte1` through `/root/.hermes/Byte14` files as automation context for Nusantara-AI News.

## Generated config

- Index/config: `/root/nusantara-ai-saas/config/byteplus-ark-automation.json`
- Regenerator: `/root/nusantara-ai-saas/scripts/byteplus-docs-index.mjs`

Run from repo:

```bash
node scripts/byteplus-docs-index.mjs
```

The regenerator verifies:
- all Byte1-Byte14 files exist
- files are sanitized and contain no literal `ark-*` bearer token
- active docs are grouped by automation stage

## Mapping

- Byte1: ARK `/chat/completions` docs for text generation and visual understanding. Used by Content Ideation / analysis prompts.
- Byte2: duplicate of Byte1; retained as reference duplicate, not primary active doc.
- Byte3: Hitem3D image-to-3D docs. Kept disabled/reference-only; not part of Shorts automation.
- Byte4: ARK `/contents/generations/tasks` Seedance video-generation API reference. Primary video automation doc.
- Byte5: ARK `/images/generations` Seedream image-generation API reference. Primary image automation doc.
- Byte6: ModelArk coding embeddings (`skylark-embedding-vision`) reference. Optional semantic dedupe/retrieval doc.
- Byte7/Byte8/Byte12/Byte14: Seedance image-to-video task examples.
- Byte13: Seedance text-to-video task example; important because Nusantara-AI video mode is prompt-only/no-reference-image.
- Byte9/Byte11: Seedream text-to-image examples.
- Byte10: SeedEdit image-to-image example.

## Env keys

```env
NEWS_BYTEPLUS_DOCS_ENABLED=1
NEWS_BYTEPLUS_DOCS_DIR=/root/.hermes
NEWS_BYTEPLUS_DOCS_INDEX_PATH=/root/nusantara-ai-saas/config/byteplus-ark-automation.json
NEWS_BYTEPLUS_CHAT_DOCS=Byte1,Byte2
NEWS_BYTEPLUS_IMAGE_DOCS=Byte5,Byte9,Byte10,Byte11
NEWS_BYTEPLUS_VIDEO_DOCS=Byte4,Byte7,Byte8,Byte12,Byte13,Byte14
NEWS_BYTEPLUS_EMBEDDING_DOCS=Byte6
ARK_BASE_URL=https://ark.ap-southeast.bytepluses.com/api/v3
SEEDANCE_BASE_URL=https://ark.ap-southeast.bytepluses.com/api/v3
ARK_IMAGE_ENDPOINT=/images/generations
SEEDANCE_TASK_ENDPOINT=/contents/generations/tasks
ARK_CHAT_ENDPOINT=/chat/completions
```

## Rules

- Never print or commit real ARK/BytePlus tokens.
- Example files must use `Authorization: Bearer $ARK_API_KEY` only.
- Byte3 remains disabled unless user asks for 3D generation.
- Image automation uses Byte5 as API source of truth and Byte9/10/11 as examples.
- Video automation uses Byte4 as API source of truth and Byte13 for prompt-only text-to-video behavior.
- Current Nusantara-AI video policy still overrides examples: no reference image by default, no OpenAI TTS, generated ambience audio, no watermark, max 30 seconds, 2×15s scenes, 9:16 1080x1920.
